from typing import Any, Dict

import models.utils as utils
import numpy as np
import tensorflow as tf
from agents import agent_registry
from core import Agent
from tensorflow.train import AdamOptimizer


@agent_registry.register('MC')
class MCAgent(Agent):
    def __init__(self, model_cls, observation_space, action_space, config=None, lr=0.001, 
                 *args, **kwargs):
        # Define parameters
        self.lr = lr

        self.policy_model = None
        self.loss = None
        self.train_q = None

        self.target_ph = utils.placeholder(shape=(1))

        super(MCAgent, self).__init__(model_cls, observation_space, action_space, config, *args, **kwargs)

    def build(self) -> None:
        self.policy_model = self.model_instances[0]
        self.loss = tf.reduce_mean((self.policy_model.values - self.target_ph) ** 2)
        self.train_q = AdamOptimizer(learning_rate=self.lr).minimize(self.loss)
        self.policy_model.sess.run(tf.global_variables_initializer())

    def learn(self, training_data: Dict[str, np.ndarray], *args, **kwargs) -> None:
        x_no_action, z, action, reward = [training_data[key] for key in ['x_no_action', 'z', 'action', 'reward']]
        x_batch = np.concatenate([x_no_action, action], axis=-1)

        self.policy_model.sess.run(self.train_q, feed_dict={
            self.policy_model.x_ph: x_batch,
            self.policy_model.z: z,
            self.target_ph: reward})

    def set_weights(self, weights, *args, **kwargs) -> None:
        self.policy_model.set_weights(weights)

    def get_weights(self, *args, **kwargs) -> Any:
        return self.policy_model.get_weights()

    def save(self, path, *args, **kwargs) -> None:
        self.policy_model.save(path)

    def load(self, path, *args, **kwargs) -> None:
        self.policy_model.load(path)
