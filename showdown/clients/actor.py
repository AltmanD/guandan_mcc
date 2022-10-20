import os
import pickle
import time
from argparse import ArgumentParser
from multiprocessing import Process

import numpy as np
import tensorflow as tf
import zmq
from pyarrow import deserialize, serialize
from tensorflow.keras.backend import set_session

from model import GDModel

parser = ArgumentParser()
parser.add_argument('--observation_space', type=int, default=(567,),
                    help='The YAML configuration file')
parser.add_argument('--action_space', type=int, default=(5, 216),
                    help='The YAML configuration file')
parser.add_argument('--model_id', type=int, default=150,
                    help='The YAML configuration file')

class Player():
    def __init__(self, args) -> None:
        # Set 'allow_growth'
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        set_session(tf.Session(config=config))

        # 数据初始化
        self.args = args
        self.init_time = time.time()

        # 模型初始化
        self.model  = GDModel(args.observation_space, (5, 216))
        with open('/home/luyd/guandan_mcc/showdown/clients/dan.ckpt', 'rb') as f:
            new_weights = pickle.load(f)
        self.model.set_weights(new_weights)
    
    def sample(self, state) -> int:
        output = self.model.forward(state['x_batch'])
        action_idx = np.argmax(output)
        return action_idx


def run_one_player(index, args):
    player = Player(args)

    # 初始化zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{6000+index}')

    action_index = 0
    while True:
        state = deserialize(socket.recv())
        action_index = player.sample(state)
        # print(f'actor{index} do action number {action_index}')
        socket.send(serialize(action_index).to_buffer())


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
    for i in [1, 2, 3]:
        print(f'start{i}')
        p = Process(target=exit_wrapper, args=(i-1, args))
        p.start()
        time.sleep(0.5)
        players.append(p)

    for player in players:
        player.join()

if __name__ == '__main__':
    main()
