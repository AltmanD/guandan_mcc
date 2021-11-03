import numpy as np
import tensorflow as tf

from models import model_registry
from pathlib import Path
from tensorflow.keras.backend import get_session
from typing import Any

__all__ = ['ACModel', 'cus_ACMLPModel', 'cus_ACCNNModel']


def placeholder(dtype=tf.float32, shape=None):
    return tf.placeholder(dtype=dtype, shape=combined_shape(None, shape))
    

def combined_shape(length, shape=None):
    if shape is None:
        return (length,)
    return (length, shape) if np.isscalar(shape) else (length, *shape)


def mlp(x, hidden_sizes=(32,), activation=tf.tanh, output_activation=None):
    for h in hidden_sizes[:-1]:
        x = tf.layers.dense(x, units=h, activation=activation)
    return tf.layers.dense(x, units=hidden_sizes[-1], activation=output_activation)


def ortho_init(scale=1.0):
    def _ortho_init(shape, dtype, partition_info=None):
        # lasagne ortho init for tf
        shape = tuple(shape)
        if len(shape) == 2:
            flat_shape = shape
        elif len(shape) == 4:  # assumes NHWC
            flat_shape = (np.prod(shape[:-1]), shape[-1])
        else:
            raise NotImplementedError
        a = np.random.normal(0.0, 1.0, flat_shape)
        u, _, v = np.linalg.svd(a, full_matrices=False)
        q = u if u.shape == flat_shape else v  # pick the one with the correct shape
        q = q.reshape(shape)
        return (scale * q[:shape[0], :shape[1]]).astype(np.float32)

    return _ortho_init


def conv(x, scope, *, nf, rf, stride, pad='VALID', init_scale=1.0, data_format='NHWC', one_dim_bias=False):
    if data_format == 'NHWC':
        channel_ax = 3
        strides = [1, stride, stride, 1]
        bshape = [1, 1, 1, nf]
    elif data_format == 'NCHW':
        channel_ax = 1
        strides = [1, 1, stride, stride]
        bshape = [1, nf, 1, 1]
    else:
        raise NotImplementedError
    bias_var_shape = [nf] if one_dim_bias else [1, nf, 1, 1]
    nin = x.get_shape()[channel_ax].value
    wshape = [rf, rf, nin, nf]
    with tf.variable_scope(scope):
        w = tf.get_variable("w", wshape, initializer=ortho_init(init_scale))
        b = tf.get_variable("b", bias_var_shape, initializer=tf.constant_initializer(0.0))
        if not one_dim_bias and data_format == 'NHWC':
            b = tf.reshape(b, bshape)
        return tf.nn.conv2d(x, w, strides=strides, padding=pad, data_format=data_format) + b


def fc(x, scope, nh, *, init_scale=1.0, init_bias=0.0):
    with tf.variable_scope(scope):
        nin = x.get_shape()[1].value
        w = tf.get_variable("w", [nin, nh], initializer=ortho_init(init_scale))
        b = tf.get_variable("b", [nh], initializer=tf.constant_initializer(init_bias))
        return tf.matmul(x, w) + b


def conv_to_fc(x):
    nh = np.prod([v.value for v in x.get_shape()[1:]])
    x = tf.reshape(x, [-1, nh])
    return x


class ACModel():
    def __init__(self, observation_space, action_space, config=None, model_id='0', *args, **kwargs):
        with tf.variable_scope(model_id):
            self.x_ph = placeholder(shape=observation_space, dtype='uint8')
            self.encoded_x_ph = tf.to_float(self.x_ph)
            self.a_ph = placeholder(dtype=tf.int32)

        self.logits = None
        self.vf = None

        session = get_session()
        self.sess = session
        self.observation_space = observation_space
        self.action_space = action_space
        self.model_id = model_id
        self.config = config

        # Build up model
        self.build()

        # Build assignment ops
        self._weight_ph = None
        self._to_assign = None
        self._nodes = None
        self._build_assign()

        # Build saver
        self.saver = tf.train.Saver(tf.trainable_variables())

        pd = CategoricalPd(self.logits)
        self.action = pd.sample()
        self.neglogp = pd.neglogp(self.action)
        self.neglogp_a = pd.neglogp(self.a_ph)
        self.entropy = pd.entropy()

    def set_weights(self, weights, *args, **kwargs) -> None:
        feed_dict = {self._weight_ph[var.name]: weight
                     for (var, weight) in zip(tf.trainable_variables(scope=self.scope), weights)}

        self.sess.run(self._nodes, feed_dict=feed_dict)

    def get_weights(self, *args, **kwargs) -> Any:
        return self.sess.run(tf.trainable_variables(self.scope))

    def save(self, path: Path, *args, **kwargs) -> None:
        self.saver.save(self.sess, str(path))

    def load(self, path: Path, *args, **kwargs) -> None:
        self.saver.restore(self.sess, str(path))

    def _build_assign(self):
        self._weight_ph, self._to_assign = dict(), dict()
        variables = tf.trainable_variables(self.scope)
        for var in variables:
            self._weight_ph[var.name] = tf.placeholder(var.value().dtype, var.get_shape().as_list())
            self._to_assign[var.name] = var.assign(self._weight_ph[var.name])
        self._nodes = list(self._to_assign.values())

    def forward(self, states: Any, *args, **kwargs) -> Any:
        return self.sess.run([self.action, self.vf, self.neglogp], feed_dict={self.x_ph: states})


@model_registry.register('custom_acmlp')
class cus_ACMLPModel(ACModel):

    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('pi'):
                self.logits = mlp(self.encoded_x_ph, [64, 64, self.action_space], tf.tanh)

            with tf.variable_scope('v'):
                self.vf = tf.squeeze(mlp(self.encoded_x_ph, [64, 64, 1], tf.tanh), axis=1)


@model_registry.register('custom_accnn')
class cus_ACCNNModel(ACModel):

    def build(self, *args, **kwargs) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('cnn_base'):
                scaled_images = tf.cast(self.encoded_x_ph, tf.float32) / 255.
                activ = tf.nn.relu
                h = activ(conv(scaled_images, 'c1', nf=32, rf=8, stride=4, init_scale=np.sqrt(2)))
                h2 = activ(conv(h, 'c2', nf=64, rf=4, stride=2, init_scale=np.sqrt(2)))
                h3 = activ(conv(h2, 'c3', nf=64, rf=3, stride=1, init_scale=np.sqrt(2)))
                h3 = conv_to_fc(h3)
                latent = activ(fc(h3, 'fc1', nh=512, init_scale=np.sqrt(2)))
                latent = tf.layers.flatten(latent)

            with tf.variable_scope('pi'):
                self.logits = fc(latent, 'pi', self.action_space, init_scale=0.01)

            with tf.variable_scope('v'):
                self.vf = tf.squeeze(fc(latent, 'vf', 1), axis=1)

class CategoricalPd:
    def __init__(self, logits):
        self.logits = logits

    def mode(self):
        return tf.argmax(self.logits, axis=-1)

    def logp(self, x):
        return -self.neglogp(x)

    def neglogp(self, x):
        # return tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.logits, labels=x)
        # Note: we can't use sparse_softmax_cross_entropy_with_logits because
        #       the implementation does not allow second-order derivatives...
        if x.dtype in {tf.uint8, tf.int32, tf.int64}:
            # one-hot encoding
            x_shape_list = x.shape.as_list()
            logits_shape_list = self.logits.get_shape().as_list()[:-1]
            for xs, ls in zip(x_shape_list, logits_shape_list):
                if xs is not None and ls is not None:
                    assert xs == ls, 'shape mismatch: {} in x vs {} in logits'.format(xs, ls)

            x = tf.one_hot(x, self.logits.get_shape().as_list()[-1])
        else:
            # already encoded
            assert x.shape.as_list() == self.logits.shape.as_list()

        return tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=x)

    def kl(self, other):
        a0 = self.logits - tf.reduce_max(self.logits, axis=-1, keepdims=True)
        a1 = other.logits - tf.reduce_max(other.logits, axis=-1, keepdims=True)
        ea0 = tf.exp(a0)
        ea1 = tf.exp(a1)
        z0 = tf.reduce_sum(ea0, axis=-1, keepdims=True)
        z1 = tf.reduce_sum(ea1, axis=-1, keepdims=True)
        p0 = ea0 / z0
        return tf.reduce_sum(p0 * (a0 - tf.log(z0) - a1 + tf.log(z1)), axis=-1)

    def entropy(self):
        a0 = self.logits - tf.reduce_max(self.logits, axis=-1, keepdims=True)
        ea0 = tf.exp(a0)
        z0 = tf.reduce_sum(ea0, axis=-1, keepdims=True)
        p0 = ea0 / z0
        return tf.reduce_sum(p0 * (tf.log(z0) - a0), axis=-1)

    def sample(self):
        u = tf.random_uniform(tf.shape(self.logits), dtype=self.logits.dtype)
        return tf.argmax(self.logits - tf.log(-tf.log(u)), axis=-1)
