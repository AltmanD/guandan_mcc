from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .utils import get_config_params


class Model(ABC):
    def __init__(self, observation_space: Any, action_space: Any, config: dict = None, model_id: str = '0',
                 *args, **kwargs) -> None:
        """
        This method MUST be called after (0.) in subclasses

        0. [IN '__init__' of SUBCLASSES] Define parameters, layers, tensors and other related variables
        1. If 'config' is not 'None', set specified configuration parameters (which appear after 'config')
        2. Build model

        :param model_id: The identifier of the model
        :param config: Configurations of hyper-parameters
        :param args: Positional configurations (ignored if specified in 'config')
        :param kwargs: Keyword configurations (ignored if specified in 'config')
        """
        self.observation_space = observation_space
        self.action_space = action_space
        self.model_id = model_id
        self.config = config

        # 1. Set configurations
        if config is not None:
            self.load_config(config)

        # 2. Build up model
        self.build()

    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        """Build the computational graph"""
        pass

    @abstractmethod
    def set_weights(self, weights: Any, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_weights(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def forward(self, states: Any, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def save(self, path: Path, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def load(self, path: Path, *args, **kwargs) -> None:
        pass

    def export_config(self) -> dict:
        """Export dictionary as configurations"""
        config_params = get_config_params(self)

        return {p: getattr(self, p) for p in config_params}

    def load_config(self, config: dict) -> None:
        """Load dictionary as configurations and build model"""
        for key, val in config.items():
            if key in get_config_params(Model.__init__):
                self.__dict__[key] = val
