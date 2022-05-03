import inspect
from typing import List


def get_config_params(obj_or_cls) -> List[str]:
    """
    Return configurable parameters in 'Agent.__init__' and 'Model.__init__' which appear after 'config'
    :param obj_or_cls: An instance of 'Agent' / 'Model' OR their corresponding classes (NOT base classes)
    :return: A list of configurable parameters
    """
    import core  # Import inside function to avoid cyclic import

    if inspect.isclass(obj_or_cls):
        if not issubclass(obj_or_cls, core.Agent) and not issubclass(obj_or_cls, core.Model):
            raise ValueError("Only accepts subclasses of 'Agent' or 'Model'")
    else:
        if not isinstance(obj_or_cls, core.Agent) and not isinstance(obj_or_cls, core.Model):
            raise ValueError("Only accepts instances 'Agent' or 'Model'")

    sig = list(inspect.signature(obj_or_cls.__init__).parameters.keys())

    config_params = []
    config_part = False
    for param in sig:
        if param == 'config':
            # Following parameters should be what we want
            config_part = True
        elif param in {'args', 'kwargs'}:
            pass
        elif config_part:
            config_params.append(param)

    return config_params
