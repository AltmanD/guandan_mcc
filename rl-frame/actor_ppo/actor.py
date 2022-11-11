import os
import time
from argparse import ArgumentParser
from multiprocessing import Process
from random import randint
from statistics import mean

import numpy as np
import tensorflow as tf
import zmq
from pyarrow import deserialize, serialize
from tensorflow.keras.backend import set_session

from model import GDModel
from utils import logger
from utils.data_trans import (create_experiment_dir, find_new_weights,
                              run_weights_subscriber)
from utils.utils import *

parser = ArgumentParser()
parser.add_argument('--ip', type=str, default='172.15.15.2',
                    help='IP address of learner server')
parser.add_argument('--data_port', type=int, default=5000,
                    help='Learner server port to send training data')
parser.add_argument('--param_port', type=int, default=5001,
                    help='Learner server port to subscribe model parameters')
parser.add_argument('--exp_path', type=str, default='/home/root/log',
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--num_saved_ckpt', type=int, default=4,
                    help='Number of recent checkpoint files to be saved')
parser.add_argument('--observation_space', type=int, default=(567,),
                    help='The YAML configuration file')
parser.add_argument('--action_space', type=int, default=(5, 216),
                    help='The YAML configuration file')
parser.add_argument('--epsilon', type=float, default=0.01,
                    help='Epsilon')

class Player():
    def __init__(self, args) -> None:
        # Set 'allow_growth'
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        set_session(tf.Session(config=config))

        # 数据初始化
        self.mb_states_no_action, self.mb_actions, self.mb_rewards, self.mb_q = [], [], [], []
        self.all_mb_states_no_action, self.all_mb_actions, self.all_mb_rewards = [], [], []
        self.args = args
        self.step = 0
        self.num_set_weight = 0
        self.send_times = 1

        # 模型初始化
        self.model_id = -1
        self.model  = GDModel(self.args.observation_space, (5, 216))

        # 连接learner
        context = zmq.Context()
        context.linger = 0  # For removing linger behavior
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f'tcp://{self.args.ip}:{self.args.data_port}')

        # log文件
        self.args.exp_path += f'/Client{args.client_index}'
        create_experiment_dir(self.args, f'Client{args.client_index}-')
        self.args.ckpt_path = self.args.exp_path / 'ckpt'
        self.args.log_path = self.args.exp_path / 'log'
        self.args.ckpt_path.mkdir()
        self.args.log_path.mkdir()
        logger.configure(str(self.args.log_path))

        # 开模型订阅
        subscriber = Process(target=run_weights_subscriber, args=(self.args, None))
        subscriber.start()

        # 初始化模型
        print('set weight start')
        model_init_flag = 0
        while model_init_flag == 0:
            new_weights, self.model_id = find_new_weights(-1, self.args.ckpt_path)
            if new_weights is not None:
                self.model.set_weights(new_weights)
                self.num_set_weight += 1
                model_init_flag = 1
        print('set weight success') 

    def sample(self, state) -> int:
        output = self.model.forward(state['x_batch'])
        if self.args.epsilon > 0 and np.random.rand() < self.args.epsilon:
            action_idx = np.random.randint(0, len(state['legal_actions']))
        else:
            action_idx = np.argmax(output)
        q = output[action_idx]
        self.step += 1
        action = state['legal_actions'][action_idx]
        self.mb_states_no_action.append(state['x_no_action'])
        self.mb_actions.append(card2array(action))
        self.mb_q.append(q)
        return action_idx
        
    def update_weight(self):
        new_weights, self.model_id = find_new_weights(self.model_id, self.args.ckpt_path)
        if new_weights is not None:
            self.model.set_weights(new_weights)

    def save_data(self, reward):
        self.mb_rewards = [[reward] for _ in range(len(self.mb_states_no_action))]
        self.all_mb_states_no_action += self.mb_states_no_action
        self.all_mb_actions += self.mb_actions
        self.all_mb_rewards += self.mb_rewards
        self.all_mb_q += self.all_mb_q

        self.mb_states_no_action = []
        self.mb_rewards = []
        self.mb_actions = []
        self.all_mb_q = []

    def send_data(self, reward):
        # 调整数据格式并发送
        data = self.prepare_training_data(reward)
        self.socket.send(serialize(data).to_buffer())
        self.socket.recv()

        # 打印log
        if self.send_times % 10000 == 0:
            self.send_times = 1
            logger.record_tabular("ep_step", self.step)
            logger.dump_tabular()
        else:
            self.send_times += 1

        # 重置数据存储
        self.step = 0
        self.mb_states_no_action, self.mb_actions, self.mb_rewards, self.mb_q = [], [], [], []
        self.all_mb_states_no_action, self.all_mb_actions, self.all_mb_rewards, self.all_mb_q = [], [], [], []

    def prepare_training_data(self, reward):
        states_no_action = np.asarray(self.all_mb_states_no_action)
        actions = np.asarray(self.all_mb_actions)
        rewards = np.asarray(self.all_mb_rewards)
        q = np.asarray(self.all_mb_q)
        if reward[0] == 'y':
            rewards += 1
        else:
            rewards -= 1
        data = [states_no_action, actions, q, rewards]
        name = ['x_no_action', 'action', 'q', 'reward']
        return dict(zip(name, data))


def run_one_player(index, args):
    args.client_index = index
    player = Player(args)

    # 初始化zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{6000+index}')

    action_index = 0
    while True:
        # 做动作到获得reward
        state = deserialize(socket.recv())
        if not isinstance(state, int) and not isinstance(state, float) and not isinstance(state, str):
            action_index = player.sample(state)
            socket.send(serialize(action_index).to_buffer())
        elif isinstance(state, str):
            socket.send(b'none')
            if state[0] == 'y':
                player.save_data(int(state[1]))
            else:
                player.save_data(-int(state[1]))
            player.send_data(state)
            player.update_weight()
        else:
            socket.send(b'none')
            player.save_data(state)


def main():
    # 参数传递
    args, _ = parser.parse_known_args()

    def exit_wrapper(index, *x, **kw):
        """Exit all actors on KeyboardInterrupt (Ctrl-C)"""
        try:
            run_one_player(index, *x, **kw)
        except KeyboardInterrupt:
            if index == 0:
                for _i, _p in enumerate(players):
                    if _i != index:
                        _p.terminate()

    players = []
    for i in range(4):
        # print(f'start{i}')
        p = Process(target=exit_wrapper, args=(i, args))
        p.start()
        time.sleep(0.5)
        players.append(p)

    for player in players:
        player.join()

if __name__ == '__main__':
    main()
