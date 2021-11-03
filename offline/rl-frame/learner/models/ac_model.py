from abc import abstractmethod, ABC
from typing import Any

import numpy as np
import tensorflow as tf

import models.utils as utils
from models import model_registry
from models.distributions import CategoricalPd
from models.tf_v1_model import TFV1Model
from models.utils import conv, fc, conv_to_fc

__all__ = ['ACModel', 'ACMLPModel', 'ACCNNModel']


class ACModel(TFV1Model, ABC):
    def __init__(self, observation_space, action_space, config=None, model_id='0', *args, **kwargs):
        with tf.variable_scope(model_id):
            self.x_ph = utils.placeholder(shape=observation_space, dtype='uint8')
            self.encoded_x_ph = tf.to_float(self.x_ph)
            self.a_ph = utils.placeholder(dtype=tf.int32)

        self.logits = None
        self.vf = None

        super(ACModel, self).__init__(observation_space, action_space, config, model_id, scope=model_id,
                                      *args, **kwargs)

        pd = CategoricalPd(self.logits)
        self.action = pd.sample()
        self.neglogp = pd.neglogp(self.action)
        self.neglogp_a = pd.neglogp(self.a_ph)
        self.entropy = pd.entropy()

    def forward(self, states: Any, *args, **kwargs) -> Any:
        return self.sess.run([self.action, self.vf, self.neglogp], feed_dict={self.x_ph: states})

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        pass


@model_registry.register('acmlp')
class ACMLPModel(ACModel):

    def build(self) -> None:
        with tf.variable_scope(self.scope):
            with tf.variable_scope('pi'):
                self.logits = utils.mlp(self.encoded_x_ph, [64, 64, self.action_space], tf.tanh)

            with tf.variable_scope('v'):
                self.vf = tf.squeeze(utils.mlp(self.encoded_x_ph, [64, 64, 1], tf.tanh), axis=1)


@model_registry.register('accnn')
class ACCNNModel(ACModel, ABC):

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
