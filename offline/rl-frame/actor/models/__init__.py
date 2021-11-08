from core.registry import Registry

model_registry = Registry('Model')

from models.ac_model import *
from models.ac_model_keras import *
from models.custom_model import *
from models.q_model import *
from models.q_model_keras import *


def get_model(args):
    """Initialize model instances"""
    model_cls = model_registry.get(args.model)
    model_instances = []

    model_instances.append(model_cls(args.observation_space, args.action_space))

    if len(model_instances) == 1:
        return model_instances[0]
    else:
        return model_instances
