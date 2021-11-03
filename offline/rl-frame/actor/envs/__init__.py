import re
from collections import defaultdict

import gym

from core.env import Env
from .atari import AtariEnv, make_atari
from .classic_control import ClassicControlEnv
from .vec_env import SubprocVecEnv, VecFrameStack, DummyVecEnv

mapping = {
    'atari': AtariEnv,
    'classic_control': ClassicControlEnv
}


def _get_gym_env_type(env_id):
    """Modified from https://github.com/openai/baselines/blob/master/baselines/run.py"""
    game_envs = defaultdict(set)

    for env in gym.envs.registry.all():
        env_type = env.entry_point.split(':')[0].split('.')[-1]
        game_envs[env_type].add(env.id)  # This is a set so add is idempotent

    if env_id in game_envs.keys():
        env_type = env_id
    else:
        env_type = None
        for g, e in game_envs.items():
            if env_id in e:
                env_type = g
                break
        if ':' in env_id:
            env_type = re.sub(r':.*', '', env_id)

    return env_type


def get_env(env_id: str, num_envs: int, **kwargs) -> Env:
    env_type = _get_gym_env_type(env_id)

    if env_type is None:
        # Non-gym environments
        env_type = env_id
        if env_type not in mapping:
            ValueError(f'Unknown environment: {env_type}')

        return mapping[env_type](**kwargs)

    elif env_type == 'atari':
        def make_thunk():
            return lambda: make_atari(env_id)

        if num_envs > 1:
            env = SubprocVecEnv([make_thunk() for _ in range(num_envs)])
        else:
            env = DummyVecEnv([make_thunk() for _ in range(num_envs)])
        env = VecFrameStack(env, 4)
        return AtariEnv(env)

    else:
        if env_type not in mapping:
            ValueError(f'Unknown environment: {env_type}')

        return mapping[env_type](env_id, **kwargs)
