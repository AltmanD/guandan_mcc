from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import tensorflow as tf
from core import Model
from tensorflow.keras.backend import get_session


class TFV1Model(Model, ABC):
    def __init__(self, observation_space: Any, action_space: Any, config=None, model_id='0', session=None, scope=None,
                 *args, **kwargs):
        self.scope = scope

        # Initialize Tensorflow session
        if session is None:
            session = get_session()
        self.sess = session

        super(TFV1Model, self).__init__(observation_space, action_space, config, model_id, *args, **kwargs)

        # Build assignment ops
        self._weight_ph = None
        self._to_assign = None
        self._nodes = None
        self._build_assign()

        # Build saver
        self.saver = tf.train.Saver(tf.trainable_variables())

    def set_weights(self, weights,  *args, **kwargs) -> None:
        feed_dict = {self._weight_ph[var.name]: weight
                     for (var, weight) in zip(tf.trainable_variables(self.scope), weights)}
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

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def forward(self, states: Any, *args, **kwargs) -> Any:
        pass
