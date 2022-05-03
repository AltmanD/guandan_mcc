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


class GDModel():
    def __init__(self, observation_space, action_space, config=None, model_id='0', session=None):
        with tf.variable_scope(model_id):
            self.x_ph = placeholder(shape=observation_space)
            # self.z = placeholder(shape=action_space)
            # self.zero = placeholder(shape=128)

        # 输出张量
        self.values = None

        # Initialize Tensorflow session
        if session is None:
            session = get_session()
        self.sess = session
        
        self.scope = model_id
        self.observation_space = observation_space
        self.action_space = action_space
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

    # def forward(self, x_batch, z):
    #     return self.sess.run(self.values, feed_dict={self.x_ph: x_batch, self.z: z})
    
    def forward(self, x_batch):
        return self.sess.run(self.values, feed_dict={self.x_ph: x_batch})

    # def forward(self, x_batch, z, zeros,*args, **kwargs):
    #     return self.sess.run(self.values, feed_dict={self.x_ph: x_batch, self.z: z, self.zero: zeros})

    # def build(self) -> None:
    #     with tf.variable_scope(self.scope):
    #         with tf.variable_scope('l1'):
    #             x = tf.unstack(self.z, 5, 1)
    #         with tf.variable_scope('l2'):
    #             lstm_cell = tf.contrib.rnn.BasicLSTMCell(128, forget_bias=1.0)
    #         with tf.variable_scope('l3'):
    #             outputs, _ = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
    #             lstm_out = outputs[-1]
    #             x = tf.concat([lstm_out, self.x_ph], axis=-1)
    #         with tf.variable_scope('v'):
    #             self.values = mlp(x, [512, 512, 512, 512, 512, 1], activation='relu',
    #                                         output_activation=None)
    
    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('v'):
                self.values = mlp(self.x_ph, [512, 512, 512, 512, 512, 1], activation='tanh',
                                            output_activation=None)


    # def build(self) -> None:
    #     with tf.variable_scope(self.scope):
    #         with tf.variable_scope('l1'):
    #             x = tf.unstack(self.z, 5, 1)
    #         with tf.variable_scope('l2'):
    #             lstm_cell = tf.contrib.rnn.BasicLSTMCell(128, forget_bias=1.0)
    #         with tf.variable_scope('l3'):
    #             outputs, _ = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
    #             #lstm_out = outputs[-1]
    #             #lstm_out = tf.zeros(outputs[-1].shape)
    #             x = tf.concat([self.zero, self.x_ph], axis=-1)
    #         with tf.variable_scope('v'):
    #             self.values = mlp(x, [512, 512, 512, 512, 512, 1], activation='elu',
    #                                         output_activation=None)
