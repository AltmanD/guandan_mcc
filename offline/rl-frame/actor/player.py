import json
import time
from multiprocessing import Process
from typing import Dict

import numpy as np
import zmq
from pyarrow import serialize
from ws4py.client.threadedclient import WebSocketClient

from models import get_model
from state import State
from utils import logger
from utils.data_trans import (create_experiment_dir, find_new_weights, run_weights_subscriber)


class Player():
    def __init__(self, args, unknown_args) -> None:
        # Set 'allow_growth'
        import tensorflow.compat.v1 as tf
        from tensorflow.keras.backend import set_session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        set_session(tf.Session(config=config))

        # 数据初始化
        self.mb_states, self.mb_actions, self.mb_rewards, self.mb_dones, self.mb_extras = [], [], [], [], []
        self.args = args
        self.unknown_args = unknown_args
        self.init_time = time().time()
        self.step = 0
        self.ip = args.ip
        self.data_port = args.data_port

        # 模型初始化
        self.model = get_model(args)
        self.model_id = -1

        # log文件
        create_experiment_dir(self.args, f'Client{args.client_index}-')
        self.args.ckpt_path = self.args.exp_path / 'ckpt'
        self.args.log_path = self.args.exp_path / 'log'
        self.args.ckpt_path.mkdir()
        self.args.log_path.mkdir()
        logger.configure(str(self.args.log_path))

        # 开模型订阅
        subscriber = Process(target=run_weights_subscriber, args=(self.args, self.unknown_args))
        subscriber.start()

        # 初始化模型
        model_init_flag = 0
        while not model_init_flag:
            new_weights, self.model_id = find_new_weights(self.model_id, self.args.ckpt_path)
            if new_weights is not None:
                self.model.set_weights(new_weights)
                model_init_flag = 1

    def sample(self, state) -> int:
        # 更新模型
        new_weights, self.model_id = find_new_weights(self.model_id, self.args.ckpt_path)
        if new_weights is not None:
            self.model.set_weights(new_weights)

        # forward 并存数据
        action, value, neglogp = self.model.forward(state)
        self.step += 1
        self.mb_states.append(state)
        self.mb_actions.append(action)
        self.mb_extras.append({'value': value, 'neglogp': neglogp})

        return action
        
    def send_data(self, over_message):
        # 连接learner
        context = zmq.Context()
        context.linger = 0  # For removing linger behavior
        socket = context.socket(zmq.REQ)
        socket.connect(f'tcp://{self.ip}:{self.data_port}')

        # 调整数据格式并发送
        data = self.prepare_training_data()
        socket.send(serialize(data).to_buffer())
        socket.recv()

        # 打印log
        logger.record_tabular("steps", self.step)
        logger.dump_tabular()

    def prepare_training_data(self) -> Dict[str, np.ndarray]:
        '''
        Change the dimension of the input data for training
        in pong, for example :  
        from
        mb_states  :  (128, 1, 84, 84, 4)
        mb_actions :  (128, 1)
        mb_dones   :  (128, 1)
        mb_rewards :  (128, 1)
        mb_extras  :  dict{'value': (128, 1), 'neglogp': (128, 1)}

        to 
        state   :  (128, 84, 84, 4)
        return  :  (128,)
        action  :  (128,)
        value   :  (128,)
        neglogp :  (128,)
        '''
        # 超参数
        gamma  =  0.99
        lam    =  0.95

        # 调整格式
        mb_states, mb_actions, mb_rewards, mb_dones, next_state, mb_extras = trajectory
        mb_values   =  np.asarray([extra_data['value'] for extra_data in mb_extras])
        mb_neglogp  =  np.asarray([extra_data['neglogp'] for extra_data in mb_extras])
        last_values =  model.forward(next_state)[1]
        mb_values   =  np.concatenate([mb_values, last_values[np.newaxis]])
        mb_deltas   =  mb_rewards + gamma * mb_values[1:] * (1.0 - mb_dones) - mb_values[:-1]

        nsteps     =  len(mb_states)
        mb_advs    =  np.zeros_like(mb_rewards)
        lastgaelam =  0
        for t in reversed(range(nsteps)):
            nextnonterminal = 1.0 - mb_dones[t]
            mb_advs[t] = lastgaelam = mb_deltas[t] + gamma * lam * nextnonterminal * lastgaelam

        def sf01(arr):
            """
            swap and then flatten axes 0 and 1
            """
            s = arr.shape
            return arr.swapaxes(0, 1).reshape(s[0] * s[1], *s[2:])

        mb_returns = mb_advs + mb_values[:-1]
        data = [sf01(arr) for arr in [mb_states, mb_returns, mb_actions, mb_values[:-1], mb_neglogp]]
        name = ['state', 'return', 'action', 'value', 'neglogp']
        return dict(zip(name, data))
    
    def play(self, state) -> int:
        action = self.sample(state)

        # TODO:将action处理成action_index
        action_index = action

        return 0


class MyClient(WebSocketClient):
    def __init__(self, url, args, unknown_args):
        super().__init__(url)
        self.state = State()
        self.player = Player(args, unknown_args, )
        self.history_hand = {0: [], 1: [], 2: [], 3:[]}

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        # 先序列化收到的消息，转为Python中的字典
        message = json.loads(str(message))
        # 调用状态对象来解析状态
        self.state.parse(message)
        if "actionList" in message:
            # 记录history
            self.history_hand[message['curPos']].append(message['curAction'][2])
            # 做动作
            state = self.prepare(message, self.history_hand)
            act_index = self.player.play(state)
            self.send(json.dumps({"actIndex": act_index}))
        if message['stage'] == 'episodeOver':
            self.player.send_data(message)
            self.history_hand = {0: [], 1: [], 2: [], 3:[]}

    def prepare(self, message, history):
        # TODO:将message和history合成state
        pass

