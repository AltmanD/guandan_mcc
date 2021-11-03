import datetime
import time
import warnings
from pathlib import Path
from typing import Tuple

import yaml

from agents import agent_registry
from core import Agent, Env
from envs import _get_gym_env_type, get_env
from models import model_registry


def init_components(args, unknown_args) -> Tuple[Env, Agent]:
    # Initialize environment
    env = get_env(args.env, args.num_envs, **unknown_args)

    # Get model class
    if args.model is not None:
        model_cls = model_registry.get(args.model)
    else:
        env_type = _get_gym_env_type(args.env)
        if env_type == 'atari':
            model_cls = model_registry.get('qcnn')
        elif env_type == 'classic_control':
            model_cls = model_registry.get('qmlp')
        else:
            raise NotImplementedError(f'No default model for environment: {args.env!r})')

    # Initialize agent
    agent_cls = agent_registry.get(args.alg)
    # 如果不便learner端构件env，将env.get_observation_space(), env.get_action_space()替换为具体值即可
    agent = agent_cls(model_cls, env.get_observation_space(), env.get_action_space(), args.agent_config, **unknown_args)

    return env, agent


def load_yaml_config(args, role_type: str) -> None:
    if role_type not in {'actor', 'learner'}:
        raise ValueError('Invalid role type')

    # Load config file
    if args.config is not None:
        with open(args.config) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    else:
        config = None

    if config is not None and isinstance(config, dict):
        if role_type in config:
            for k, v in config[role_type].items():
                if k in args:
                    setattr(args, k, v)
                else:
                    warnings.warn(f"Invalid config item '{k}' ignored", RuntimeWarning)
        args.agent_config = config['agent'] if 'agent' in config else None
    else:
        args.agent_config = None


def save_yaml_config(config_path: Path, args, role_type: str, agent: Agent) -> None:
    class Dumper(yaml.Dumper):
        def increase_indent(self, flow=False, *_, **__):
            return super().increase_indent(flow=flow, indentless=False)

    if role_type not in {'actor', 'learner'}:
        raise ValueError('Invalid role type')

    with open(config_path, 'w') as f:
        args_config = {k: v for k, v in vars(args).items() if
                       not k.endswith('path') and k != 'agent_config' and k != 'config'}
        yaml.dump({role_type: args_config}, f, sort_keys=False, Dumper=Dumper)
        f.write('\n')
        yaml.dump({'agent': agent.export_config()}, f, sort_keys=False, Dumper=Dumper)


def create_experiment_dir(args, prefix: str) -> None:
    if args.exp_path is None:
        args.exp_path = prefix + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    args.exp_path = Path(args.exp_path)

    if args.exp_path.exists():
        raise FileExistsError(f'Experiment directory {str(args.exp_path)!r} already exists')

    args.exp_path.mkdir()
