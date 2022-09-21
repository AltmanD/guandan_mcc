from abc import ABC, abstractmethod
from typing import Any

import tensorflow as tf

import models.utils as utils
from models import model_registry
from models.tf_v1_model import TFV1Model

__all__ = ['QModel', 'QMLPModel', 'QCNNModel', 'GDModel']


class QModel(TFV1Model, ABC):
    def __init__(self, observation_space, action_space, config=None, model_id='0', *args, **kwargs):
        with tf.variable_scope(model_id):
            self.x_ph = utils.placeholder(shape=observation_space)

        # 输出张量
        self.values = None

        # init中调用了build函数
        super(QModel, self).__init__(observation_space, action_space, config, model_id, scope=model_id,
                                     *args, **kwargs)

        # 参数初始化
        self.sess.run(tf.global_variables_initializer())    

    def forward(self, x_batch: Any, z: Any, *args, **kwargs) -> Any:
        return self.sess.run(self.values, feed_dict={self.x_ph: x_batch})

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        pass


@model_registry.register('guandan_model')
class GDModel(QModel):
    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('v'):
                self.values = utils.mlp(self.x_ph, [512, 512, 512, 512, 512, 1], activation='tanh',
                                            output_activation=None)
        print('model build success')
          

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
