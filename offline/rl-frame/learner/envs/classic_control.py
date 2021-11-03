from typing import Any, Tuple

import gym

from core.env import Env


class ClassicControlEnv(Env):
    def __init__(self, gym_env_id, *args, **kwargs):
        super(ClassicControlEnv, self).__init__(*args, **kwargs)
        self.env_wrapper = gym.make(gym_env_id)

    def step(self, action: Any, *args, **kwargs) -> Tuple[Any, Any, Any, Any]:
        return self.env_wrapper.step(action)

    def reset(self, *args, **kwargs) -> Any:
        return self.env_wrapper.reset()

    def get_action_space(self) -> Any:
        return self.env_wrapper.action_space.n

    def get_observation_space(self) -> Any:
        return self.env_wrapper.observation_space.shape[0]

    def calc_reward(self, *args, **kwargs) -> Any:
        raise NotImplemented

    def render(self, *args, **kwargs) -> None:
        self.env_wrapper.render()

    def close(self) -> None:
        self.env_wrapper.close()
