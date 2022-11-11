import numpy as np
import tensorflow as tf
from tensorflow.keras.backend import get_session


def combined_shape(length, shape=None):
    if shape is None:
        return (length,)
    return (length, shape) if np.isscalar(shape) else (length, *shape)


def placeholder(dtype=tf.float32, shape=None):
    return tf.placeholder(dtype=dtype, shape=combined_shape(None, shape))


def mlp(x, hidden_sizes=(32,), activation=tf.tanh, output_activation=None):
    for h in hidden_sizes[:-1]:
        x = tf.layers.dense(x, units=h, activation=activation)
    return tf.layers.dense(x, units=hidden_sizes[-1], activation=output_activation)


class GDPPOModel():
    def __init__(self, observation_space, config=None, model_id='0', session=None):
        with tf.variable_scope(model_id):
            self.x_ph = placeholder(shape=observation_space)
            self.x_s_ph = tf.expand_dims(self.x_ph[0, :-54], axis=0)
            self.a_ph = placeholder(dtype=tf.int32)

        # 输出张量
        self.logits = None
        self.value = None

        # Initialize Tensorflow session
        if session is None:
            session = get_session()
        self.sess = session
        
        self.scope = model_id
        self.observation_space = observation_space
        self.model_id = model_id
        self.config = config

        # Set configurations
        if config is not None:
            self.load_config(config)

        # Build up model
        self.build()

        # Build assignment ops
        self._weight_ph = None
        self._to_assign = None
        self._nodes = None
        self._build_assign()

        # Build saver
        self.saver = tf.train.Saver(tf.trainable_variables())

        # 参数初始化
        self.sess.run(tf.global_variables_initializer())    

    def set_weights(self, weights) -> None:
        feed_dict = {self._weight_ph[var.name]: weight
                     for (var, weight) in zip(tf.trainable_variables(self.scope), weights)}
        self.sess.run(self._nodes, feed_dict=feed_dict)

    def get_weights(self):
        return self.sess.run(tf.trainable_variables(self.scope))

    def save(self, path) -> None:
        self.saver.save(self.sess, str(path))

    def load(self, path) -> None:
        self.saver.restore(self.sess, str(path))

    def _build_assign(self):
        self._weight_ph, self._to_assign = dict(), dict()
        variables = tf.trainable_variables(self.scope)
        for var in variables:
            self._weight_ph[var.name] = tf.placeholder(var.value().dtype, var.get_shape().as_list())
            self._to_assign[var.name] = var.assign(self._weight_ph[var.name])
        self._nodes = list(self._to_assign.values())

    def forward(self, x_batch):
        self.logits, self.value = self.sess.run([self.logits, self.value], feed_dict={self.x_ph: x_batch})
        self.logits = tf.convert_to_tensor(np.expand_dims(self.logits.flatten(), axis=0))
        # print(self.logits)
        self.action = self.sample()
        self.neglogp = self.Neglogp(self.action)
        action, neglogp = self.sess.run([self.action, self.neglogp])
        return action, self.value, neglogp
        return self.sess.run([self.logits, self.value], feed_dict={self.x_ph: x_batch})

    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('p'):
                self.logits = mlp(self.x_ph, [512, 512, 512, 512, 512, 1], activation='tanh',
                                            output_activation=None)
            with tf.variable_scope('v'):
                self.value = mlp(self.x_s_ph, [512, 512, 512, 512, 512, 1], activation='tanh',
                                            output_activation=None)


class CategoricalPd:
    def __init__(self, session=None):
        self.model = GDPPOModel(observation_space=(567, ))
        self.logits = None
        if session is None:
            session = get_session()
        self.sess = session

    def forward(self, x_batch):
        self.logits, value = self.model.forward(x_batch)
        self.logits = tf.convert_to_tensor(np.expand_dims(self.logits.flatten(), axis=0))
        # print(self.logits)
        self.action = self.sample()
        self.neglogp = self.Neglogp(self.action)
        action, neglogp = self.sess.run([self.action, self.neglogp])
        return action, value, neglogp

    def set_weights(self, weights) -> None:
        self.model.set_weights(weights)

    def get_weights(self):
        return self.model.get_weights()

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model.load(path)

    def mode(self):
        return tf.argmax(self.logits, axis=-1)

    def logp(self, x):
        return -self.Neglogp(x)

    def Neglogp(self, x):
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

if __name__ == '__main__':
    policy = CategoricalPd()
    state = np.random.random((513, ))
    action1 = np.random.random((54, ))
    action2 = np.random.random((54, ))
    action3 = np.random.random((54, ))
    # print(np.concatenate((state,action1), axis=0))
    res = policy.forward([np.concatenate((state,action1), axis=0), np.concatenate((state,action2), axis=0), np.concatenate((state,action3), axis=0)])
    print(res)
    # print(policy.forward([np.random.random((567, )), np.random.random((567, ))]))
