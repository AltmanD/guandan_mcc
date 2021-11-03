import os
import time
from argparse import ArgumentParser
from collections import deque
from itertools import count
from multiprocessing import Array, Process

import numpy as np
import zmq
from pyarrow import serialize

from envs import get_env
from models import get_model
from utils import logger
from utils.cmdline import parse_cmdline_kwargs
from utils.data_trans import (create_experiment_dir, find_new_weights,
                              load_yaml_config, prepare_training_data)

parser = ArgumentParser()
parser.add_argument('--alg', type=str, default='ppo', help='The RL algorithm')
parser.add_argument('--env', type=str, default='PongNoFrameskip-v4', help='The game environment')
parser.add_argument('--num_steps', type=int, default=10000000, help='The number of total training steps')
parser.add_argument('--ip', type=str, default='127.0.0.1', help='IP address of learner server')
parser.add_argument('--data_port', type=int, default=5000, help='Learner server port to send training data')
parser.add_argument('--param_port', type=int, default=5001, help='Learner server port to subscribe model parameters')
parser.add_argument('--num_replicas', type=int, default=10, help='The number of actors')
parser.add_argument('--model', type=str, default='accnn', help='Training model')
parser.add_argument('--max_steps_per_update', type=int, default=128,
                    help='The maximum number of steps between each update')
parser.add_argument('--exp_path', type=str, default=None,
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--num_saved_ckpt', type=int, default=10, help='Number of recent checkpoint files to be saved')
parser.add_argument('--max_episode_length', type=int, default=1000, help='Maximum length of trajectory')
parser.add_argument('--config', type=str, default=None, help='The YAML configuration file')
parser.add_argument('--use_gpu', action='store_true', help='Use GPU to sample every action')
parser.add_argument('--num_envs', type=int, default=1, help='The number of environment copies')


def run_one_actor(index, args, unknown_args, actor_status):
    import tensorflow.compat.v1 as tf
    from tensorflow.keras.backend import set_session

    # Set 'allow_growth'
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    set_session(tf.Session(config=config))

    # Connect to learner
    context = zmq.Context()
    context.linger = 0  # For removing linger behavior
    socket = context.socket(zmq.REQ)
    socket.connect(f'tcp://{args.ip}:{args.data_port}')

    # Initialize environment and model instance
    env = get_env(args.env, args.num_envs, **unknown_args)
    model = get_model(env, args)

    # Configure logging only in one process
    if index == 0:
        logger.configure(str(args.log_path))
    else:
        logger.configure(str(args.log_path), format_strs=[])

    # Initialize values
    model_id = -1
    episode_infos = deque(maxlen=100)
    num_episode = 0
    state = env.reset()

    nupdates = args.num_steps // args.max_steps_per_update

    model_init_flag = 0
    for update in range(1, nupdates + 1):
        # Update weights
        new_weights, model_id = find_new_weights(model_id, args.ckpt_path)
        if new_weights is not None:
            model.set_weights(new_weights)
            model_init_flag = 1
        elif model_init_flag == 0:
            continue

        # Collect data
        mb_states, mb_actions, mb_rewards, mb_dones, mb_extras = [], [], [], [], []
        start_time = time.time()
        for _ in range(args.max_steps_per_update):

            mb_states.append(state)

            # Sample action
            action, value, neglogp = model.forward(state)
            extra_data = {'value': value, 'neglogp': neglogp}
            state, reward, done, info = env.step(action)

            mb_actions.append(action)
            mb_rewards.append(reward)
            mb_dones.append(done)
            mb_extras.append(extra_data)

            for info_i in info:
                maybeepinfo = info_i.get('episode')
                if maybeepinfo:
                    episode_infos.append(maybeepinfo)
                    num_episode += 1

        mb_states  =  np.asarray(mb_states, dtype=state.dtype)
        mb_rewards =  np.asarray(mb_rewards, dtype=np.float32)
        mb_actions =  np.asarray(mb_actions)
        mb_dones   =  np.asarray(mb_dones, dtype=np.bool)

        # Adjust data format and send to learner
        data = prepare_training_data(model, [mb_states, mb_actions, mb_rewards, mb_dones, state, mb_extras])
        socket.send(serialize(data).to_buffer())
        socket.recv()

        send_data_interval = time.time() - start_time
        # Log information
        logger.record_tabular("steps", update * args.max_steps_per_update)
        logger.record_tabular("episodes", num_episode)
        logger.record_tabular("mean 100 episode reward",
                              round(np.mean([epinfo['reward'] for epinfo in episode_infos]), 2))
        logger.record_tabular("mean 100 episode length",
                              round(np.mean([epinfo['length'] for epinfo in episode_infos]), 2))
        logger.record_tabular("send data interval", send_data_interval)
        logger.record_tabular("send data fps", args.max_steps_per_update // send_data_interval)
        logger.record_tabular("total steps", nupdates * args.max_steps_per_update)
        logger.dump_tabular()

    actor_status[index] = 1


def run_weights_subscriber(args, actor_status):
    """Subscribe weights from Learner and save them locally"""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f'tcp://{args.ip}:{args.param_port}')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe everything

    for model_id in count(1):  # Starts from 1
        while True:
            try:
                weights = socket.recv(flags=zmq.NOBLOCK)

                # Weights received
                with open(args.ckpt_path / f'{model_id}.{args.alg}.{args.env}.ckpt', 'wb') as f:
                    f.write(weights)

                if model_id > args.num_saved_ckpt:
                    os.remove(args.ckpt_path / f'{model_id - args.num_saved_ckpt}.{args.alg}.{args.env}.ckpt')
                break
            except zmq.Again:
                pass

            if all(actor_status):
                # All actors finished works
                return

            # For not cpu-intensive
            time.sleep(1)


def main():
    # Parse input parameters
    args, unknown_args = parser.parse_known_args()
    args.num_steps = int(args.num_steps)
    unknown_args = parse_cmdline_kwargs(unknown_args)

    # Load config file
    load_yaml_config(args, 'actor')

    # Create experiment directory
    create_experiment_dir(args, 'ACTOR-')

    args.ckpt_path = args.exp_path / 'ckpt'
    args.log_path = args.exp_path / 'log'
    args.ckpt_path.mkdir()
    args.log_path.mkdir()

    # Record commit hash
    # with open(args.exp_path / 'hash', 'w') as f:
    #     f.write(str(subprocess.run('git rev-parse HEAD'.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')))

    # Disable GPU
    if not args.use_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    # Running status of actors
    actor_status = Array('i', [0] * args.num_replicas)

    # Run weights subscriber
    subscriber = Process(target=run_weights_subscriber, args=(args, actor_status))
    subscriber.start()

    def exit_wrapper(index, *x, **kw):
        """Exit all actors on KeyboardInterrupt (Ctrl-C)"""
        try:
            run_one_actor(index, *x, **kw)
        except KeyboardInterrupt:
            if index == 0:
                for _i, _p in enumerate(actors):
                    if _i != index:
                        _p.terminate()
                    actor_status[_i] = 1

    actors = []
    for i in range(args.num_replicas):
        p = Process(target=exit_wrapper, args=(i, args, unknown_args, actor_status))
        p.start()
        os.system(f'taskset -p -c {i % os.cpu_count()} {p.pid}')  # For CPU affinity

        actors.append(p)

    for actor in actors:
        actor.join()

    subscriber.join()


if __name__ == '__main__':
    main()
