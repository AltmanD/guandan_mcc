from abc import ABC, abstractmethod
from typing import Any, Tuple


class Env(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def step(self, action: Any, *args, **kwargs) -> Tuple[Any, Any, Any, Any]:
        pass

    @abstractmethod
    def reset(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_action_space(self) -> Any:
        pass

    @abstractmethod
    def get_observation_space(self) -> Any:
        pass

    @abstractmethod
    def calc_reward(self, *args, **kwargs) -> Any:
        """Reshape rewards"""
        pass

    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
