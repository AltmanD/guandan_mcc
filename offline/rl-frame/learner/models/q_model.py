from abc import abstractmethod, ABC
from typing import Any

import tensorflow as tf

import models.utils as utils
from models import model_registry
from models.tf_v1_model import TFV1Model

__all__ = ['QModel', 'QMLPModel', 'QCNNModel']


class QModel(TFV1Model, ABC):
    def __init__(self, observation_space, action_space, config=None, model_id='0', *args, **kwargs):
        with tf.variable_scope(model_id):
            self.x_ph = utils.placeholder(shape=observation_space)
            self.z = utils.placeholder(shape=(None, 5, 162))

        # Output tensors
        self.values = None

        super(QModel, self).__init__(observation_space, action_space, config, model_id, scope=model_id,
                                     *args, **kwargs)

    def forward(self, x_batch, z, *args, **kwargs) -> Any:
        return self.sess.run(self.values, feed_dict={self.x_ph: x_batch, self.z: z})

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        pass


@model_registry.register('guandan_model')
class GDModel(QModel):
    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('z'):
                lstm_cell = tf.contrib.rnn.BasicLSTMCell(128)
                outputs, _ = tf.contrib.rnn.static_rnn(lstm_cell, self.z, dtype=tf.float32)
                lstm_out = outputs[:,-1,:]
                x = tf.concat([lstm_out, self.x_ph], dim=-1)
            with tf.variable_scope('q'):
                self.values = utils.mlp(x, [512, 512, 512, 512, 512, 1], activation='relu',
                                        output_activation=None)


@model_registry.register('qmlp')
class QMLPModel(QModel):
    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('q'):
                self.values = utils.mlp(self.x_ph, [24, 24, self.action_space], activation='relu',
                                        output_activation=None)


@model_registry.register('qcnn')
class QCNNModel(QModel):
    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('cnn_base'):
                layers = [{'filters': 16, 'kernel_size': 8, 'strides': 4, 'activation': 'relu'},
                          {'filters': 32, 'kernel_size': 4, 'strides': 2, 'activation': 'relu'}]
                feat = self.x_ph
                for layer in layers:
                    feat = tf.layers.conv2d(feat, **layer)
                feat = tf.layers.flatten(feat)
            with tf.variable_scope('q'):
                self.values = utils.mlp(feat, [256, self.action_space], activation='relu',
                                        output_activation=None)
