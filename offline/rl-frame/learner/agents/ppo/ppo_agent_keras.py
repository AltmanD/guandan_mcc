from pathlib import Path
from typing import Tuple, Any, Dict, List

import numpy as np
import scipy.signal
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import optimizers

from agents import agent_registry
from core import Agent
from models import TFKerasModel


@agent_registry.register('ppok')
class PPOKerasAgent(Agent):
    def __init__(self, model_cls, observation_space, action_space, config=None, gamma=0.97, lam=0.98, lr=1e-4,
                 buffer_size=0, clip_range=0.2, ent_coef=1e-2, epochs=10, verbose=False, *args, **kwargs):
        assert issubclass(model_cls, TFKerasModel)

        # Define parameters
        self.gamma = gamma
        self.lam = lam
        self.lr = lr
        self.buffer_size = buffer_size
        self.clip_range = clip_range
        self.ent_coef = ent_coef
        self.epochs = epochs
        self.verbose = verbose

        # Default model config
        if config is None:
            config = {'model': [{'model_id': 'policy_model'}]}

        self.model = None

        super(PPOKerasAgent, self).__init__(model_cls, observation_space, action_space, config, *args, **kwargs)

    def build(self) -> None:
        self.model = self.model_instances[0]
        self.model.model.compile(optimizer=optimizers.Adam(lr=self.lr), loss=[self._actor_loss, "huber_loss"])

    def _actor_loss(self, act_adv_prob, y_pred):
        action, advantage, action_prob = [tf.reshape(x, [-1]) for x in tf.split(act_adv_prob, 3, axis=-1)]
        action = tf.cast(action, tf.int32)
        index = tf.transpose(tf.stack([tf.range(tf.shape(action)[0]), action]))
        prob = tf.gather_nd(y_pred, index)

        r = prob / (action_prob + 1e-10)

        return -K.mean(K.minimum(r * advantage, K.clip(r, min_value=1 - self.clip_range,
                                                       max_value=1 + self.clip_range) * advantage) +
                       self.ent_coef * K.sum(- y_pred * K.log(y_pred + 1e-10), -1))

    def sample(self, state: Any, *args, **kwargs) -> Tuple[Any, dict]:
        action_probs, value = self.model.forward(state[np.newaxis])
        action_probs = np.squeeze(action_probs)
        action = np.random.choice(np.arange(self.action_space), p=np.squeeze(action_probs))
        return action, {'act_prob': action_probs[action], 'value': value.item()}

    def learn(self, training_data: Dict[str, np.ndarray], *args, **kwargs) -> None:
        states, actions, act_probs, values, advantages = [
            training_data[key] for key in ['state', 'action', 'act_prob', 'value', 'advantage']
        ]

        act_adv_prob = np.stack([actions, advantages, act_probs], axis=-1)
        self.model.model.fit([states], [act_adv_prob, values + advantages], epochs=self.epochs, verbose=self.verbose)

    def prepare_training_data(self, trajectory: List[Tuple[Any, Any, Any, Any, bool, dict]]) -> Dict[str, np.ndarray]:
        states, actions, rewards = [np.array(i) for i in list(zip(*trajectory))[:3]]
        next_state = trajectory[-1][3]
        done = trajectory[-1][4]

        extra_data = [i[-1] for i in trajectory]
        values = np.array([x['value'] for x in extra_data])

        last_val = (1 - done) * self.model.forward(next_state[np.newaxis])[1].item()
        values = np.append(values, last_val)
        deltas = rewards + self.gamma * values[1:] - values[:-1]

        advantages = discount_cumulative_sum(deltas, self.gamma * self.lam)

        return {
            'state': states,
            'action': actions,
            'value': values[:-1],
            'act_prob': np.array([x['act_prob'] for x in extra_data]),
            'advantage': advantages
        }

    def post_process_training_data(self, training_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        return training_data

    def set_weights(self, weights, *args, **kwargs) -> None:
        self.model.set_weights(weights)

    def get_weights(self, *args, **kwargs) -> Any:
        return self.model.get_weights()

    def save(self, path: Path, *args, **kwargs) -> None:
        self.model.model.save(path)

    def load(self, path: Path, *args, **kwargs) -> None:
        self.model.model.load(path)

    def preprocess(self, state: Any, *args, **kwargs) -> Any:
        pass

    def update_sampling(self, current_step: int, total_steps: int, *args, **kwargs) -> None:
        pass

    def update_training(self, current_step: int, total_steps: int, *args, **kwargs) -> None:
        pass


def discount_cumulative_sum(x, discount):
    """
    Magic from RLLab for computing discounted cumulative sums of vectors.
    :param x: [x0, x1, x2]
    :param discount: Discount coefficient
    :return: [x0 + discount * x1 + discount^2 * x2, x1 + discount * x2, x2]
    """

    return scipy.signal.lfilter([1], [1, float(-discount)], x[::-1], axis=0)[::-1]
