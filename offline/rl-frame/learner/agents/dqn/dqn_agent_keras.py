from typing import Any, Tuple, Dict, List

import numpy as np
from tensorflow.keras.optimizers import Adam

from agents import agent_registry
from core import Agent


@agent_registry.register('dqnk')
class DQNKerasAgent(Agent):
    def __init__(self, model_cls, observation_space, action_space, config=None, gamma=0.99, lr=0.001, epochs=1,
                 epsilon=1, epsilon_min=0.01, exploration_fraction=0.1, update_freq=1000, training_start=5000,
                 verbose=False, *args, **kwargs):
        # Define parameters
        self.gamma = gamma
        self.lr = lr
        self.epochs = epochs
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.exploration_fraction = exploration_fraction
        self.update_freq = update_freq
        self.training_start = training_start
        self.verbose = verbose

        # Default model config
        if config is None:
            config = {'model': [{'model_id': 'policy_model'}, {'model_id': 'target_model'}]}

        self.policy_model = None
        self.target_model = None
        self.train = False

        super(DQNKerasAgent, self).__init__(model_cls, observation_space, action_space, config, *args, **kwargs)

    def build(self) -> None:
        self.policy_model = self.model_instances[0]
        self.target_model = self.model_instances[1]

        # Compile model
        optimizer = Adam(learning_rate=self.lr)
        self.policy_model.model.compile(loss='mean_squared_error', optimizer=optimizer)
        self.update_target_model()

    def learn(self, training_data: Dict[str, np.ndarray], *args, **kwargs) -> None:
        if self.train:
            states, next_states, actions = [training_data[key] for key in ['state', 'next_state', 'action']]
            idx = np.arange(len(actions))

            next_action = np.argmax(self.policy_model.forward(next_states), axis=-1)
            next_val = self.target_model.forward(next_states)[idx, next_action]

            target = training_data['reward'] + (1 - training_data['done']) * self.gamma * next_val
            target_f = self.policy_model.forward(states)
            target_f[idx, actions] = target
            self.policy_model.model.fit(states, target_f, epochs=self.epochs, verbose=self.verbose)

    def sample(self, state: Any, *args, **kwargs) -> Tuple[Any, dict]:
        if np.random.rand() <= self.epsilon:
            action = np.random.randint(self.action_space)
        else:
            act_values = self.policy_model.forward(state[np.newaxis])
            action = np.argmax(act_values[0])
        return action, {}

    def prepare_training_data(self, trajectory: List[Tuple[Any, Any, Any, Any, bool, dict]]) -> Dict[str, np.ndarray]:
        states, actions, rewards, next_states, dones = [np.array(i) for i in list(zip(*trajectory))[:5]]
        return {
            'state': states,
            'action': actions,
            'reward': rewards,
            'next_state': next_states,
            'done': dones
        }

    def post_process_training_data(self, training_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        return training_data

    def preprocess(self, state: Any, *args, **kwargs) -> Any:
        pass

    def set_weights(self, weights, *args, **kwargs) -> None:
        self.policy_model.set_weights(weights)
        self.update_target_model()

    def get_weights(self, *args, **kwargs) -> Any:
        return self.policy_model.get_weights()

    def update_sampling(self, current_step: int, total_steps: int, *args, **kwargs) -> None:
        # Adjust Epsilon
        fraction = min(1.0, float(current_step) / (total_steps * self.exploration_fraction))
        self.epsilon = 1 + fraction * (self.epsilon_min - 1)

    def update_training(self, current_step: int, total_steps: int, *args, **kwargs) -> None:
        if current_step > self.training_start and current_step % self.update_freq == 0:
            self.update_target_model()
        if not self.train and current_step > self.training_start:
            self.train = True

    def save(self, path, *args, **kwargs) -> None:
        self.policy_model.save(path)

    def load(self, path, *args, **kwargs) -> None:
        self.policy_model.load(path)

    def update_target_model(self):
        self.target_model.set_weights(self.policy_model.get_weights())
