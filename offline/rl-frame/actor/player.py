import json
import os
import time
from argparse import ArgumentParser
from collections import Counter
from functools import reduce
from multiprocessing import Process
from typing import Dict
from random import randint


import numpy as np
import zmq
from pyarrow import serialize
from ws4py.client.threadedclient import WebSocketClient
from models import get_model
from state import State
from utils import logger
from utils.rule import combine_handcards
from utils.data_trans import (create_experiment_dir, find_new_weights,
                              run_weights_subscriber)

CardToNum = {
    'H2':0, 'H3':1, 'H4':2, 'H5':3, 'H6':4, 'H7':5, 'H8':6, 'H9':7, 'HT':8, 'HJ':9, 'HQ':10, 'HK':11, 'HA':12,
    'S2':13, 'S3':14, 'S4':15, 'S5':16, 'S6':17, 'S7':18, 'S8':19, 'S9':20, 'ST':21, 'SJ':22, 'SQ':23, 'SK':24, 'SA':25,
    'C2':26, 'C3':27, 'C4':28, 'C5':29, 'C6':30, 'C7':31, 'C8':32, 'C9':33, 'CT':34, 'CJ':35, 'CQ':36, 'CK':37, 'CA':38,
    'D2':39, 'D3':40, 'D4':41, 'D5':42, 'D6':43, 'D7':44, 'D8':45, 'D9':46, 'DT':47, 'DJ':48, 'DQ':49, 'DK':50, 'DA':51,
    'SB':52, 'HR':53
}

RANK = {
    '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8,
    'T':9, 'J':10, 'Q':11, 'K':12, 'A':13
}

def card2num(list_cards):      # 将字符串转换成数字
    res = []   
    if list_cards == None:
        return res
    for ele in list_cards:
        if ele in CardToNum:
            res.append(CardToNum[ele])
    return res

def card2array(list_cards):
    if len(list_cards) == 0:
        return np.zeros(54, dtype=np.int8)
    matrix = np.zeros([4, 13], dtype=np.int8)
    jokers = np.zeros(2, dtype=np.int8)
    counter = Counter(list_cards)
    for card, num_times in counter.items():
        if card < 52:
            matrix[card // 13, card % 13] = num_times
        elif card == 52:
            jokers[0] = num_times
        elif card == 53:
            jokers[1] = num_times
    return np.concatenate((matrix.flatten('F'), jokers))

def _get_one_hot_array(num_left_cards, max_num_cards):
    one_hot = np.zeros(max_num_cards)
    one_hot[num_left_cards - 1] = 1

    return one_hot

def _action_seq_list2array(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 54))
    for row, list_cards in enumerate(action_seq_list):
        action_seq_array[row, :] = card2array(list_cards)
    action_seq_array = action_seq_array.reshape(5, 216)
    return action_seq_array

def _process_action_seq(sequence, length=20):
    sequence = sequence[-length:].copy()
    if len(sequence) < length:
        empty_sequence = [[] for _ in range(length - len(sequence))]
        empty_sequence.extend(sequence)
        sequence = empty_sequence
    return sequence


class Player():
    def __init__(self, args, unknown_args) -> None:
        # Set 'allow_growth'
        import tensorflow.compat.v1 as tf
        from tensorflow.keras.backend import set_session
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
        tf.logging.set_verbosity(tf.logging.ERROR)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        set_session(tf.Session(config=config))

        # 数据初始化
        self.mb_states_no_action, self.mb_z, self.mb_actions, self.mb_rewards = [], [], [], []
        self.args = args
        self.unknown_args = unknown_args
        self.init_time = time.time()
        self.step = 0
        self.ip = args.ip
        self.data_port = args.data_port
        self.size = 0
        self.epsilon = args.epsilon

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
        while model_init_flag == 0:
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
        output= self.model.forward(state['x_batch'], state['z_batch'])
        if self.epsilon > 0 and np.random.rand() < self.epsilon:
            action_idx = np.random.randint(0, len(state['legal_actions']))
        else:
            action_idx = np.argmax(output)
        self.step += 1
        action = state['legal_actions'][action_idx]
        self.mb_states_no_action.append(state['x_no_action'])
        self.mb_z.append(state['z'])
        self.mb_actions.append([action])
        self.size += 1
        return action_idx
        
    def send_data(self, reward):
        # 连接learner
        context = zmq.Context()
        context.linger = 0  # For removing linger behavior
        socket = context.socket(zmq.REQ)
        socket.connect(f'tcp://{self.ip}:{self.data_port}')

        # 调整数据格式并发送
        data = self.prepare_training_data(reward)
        socket.send(serialize(data).to_buffer())
        socket.recv()

        # 打印log
        logger.record_tabular("steps", self.step)
        logger.dump_tabular()

        # 重置数据存储
        self.size = 0
        self.mb_states_no_action = []
        self.mb_z = []
        self.rewards = []
        self.mb_actions = []

    def prepare_training_data(self, reward) -> Dict[str, np.ndarray]:
        self.rewards = [[reward] for _ in range(self.size)]
        mb_states_no_action = np.asarray(self.mb_states_no_action)
        mb_z = np.asarray(self.mb_z)
        mb_actions = np.asarray(self.mb_actions)
        rewards = np.asarray(self.rewards)
        data = [mb_states_no_action, mb_z, mb_actions, rewards]
        name = ['x_no_action', 'z', 'action', 'reward']
        return dict(zip(name, data))
    
    def play(self, state) -> int:
        action_idx = self.sample(state)
        return action_idx

    # 进还贡
    def back_action(self, msg, mypos, tribute_result):
        rank = msg["curRank"]
        self.action = msg["actionList"]
        handCards = msg["handCards"]
        card_val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                    "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
        card_val[rank] = 15
        def flag_TJQ(handCards_X) -> tuple:
            flag_T = False
            flag_J = False
            flag_Q = False
            for i in range(len(handCards_X)):
                if handCards_X[i][0][-1] == "T":
                    flag_T = True
                if handCards_X[i][0][-1] == "J":
                    flag_J = True
                if handCards_X[i][0][-1] == "Q":
                    flag_Q = True
            return flag_T, flag_J, flag_Q

        def get_card_index(target: str) -> int:
            for i in range(len(self.action)):
                if self.action[i][2][0] == target:
                    return i

        def choose_in_single(single_list) -> str:
            for my_pos in tribute_result:
                if my_pos[1] == mypos:
                    tribute_pos = my_pos[0]

            n = len(single_list)
            if (int(tribute_pos) + int(mypos)) % 2 != 0:  
                for card in single_list:
                    if card in ['H5', 'HT']:  
                        return card
                    elif card in ['S5', 'C5', 'D5', 'ST', 'CT', 'DT']:
                        return card  
                
                return single_list[randint(0, n - 1)]
            else:  
                back_list = []
                for card in single_list:
                    if card[-1] != 'T':
                        if int(card[-1]) < 5:
                            back_list.append(card)  
                if back_list:
                    return back_list[randint(0, len(back_list) - 1)]
                return single_list[randint(0, n - 1)]

        def choose_in_pair(pair_list, pair_list_from_handcards) -> str:
            val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
            if len(pair_list) < 3:
                return pair_list[0][0]
            for i in range(len(pair_list)):
                flag = False
                if i >= 2:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i - 2][0][-1], pair_list[i - 1][0][-1], \
                                                                      pair_list[i][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if 1 <= i <= len(pair_list) - 2:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i - 1][0][-1], pair_list[i][0][-1], \
                                                                      pair_list[i + 1][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if i <= len(pair_list) - 3:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i][0][-1], pair_list[i + 1][0][-1], \
                                                                      pair_list[i + 2][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if pair_list[i][0][-1] == '9':
                    flag_T, flag_J, flag_Q = flag_TJQ(pair_list_from_handcards)
                    if flag_T and flag_J:
                        flag = True
                if pair_list[i][0][-1] == 'T':
                    flag_T, flag_J, flag_Q = flag_TJQ(pair_list_from_handcards)
                    if flag_J and flag_Q:
                        flag = True
                if flag:
                    continue
                else:
                    return pair_list[i][0]
            return pair_list[0][0]

        def choose_in_trips(trips_list, trips_list_from_handcards) -> str:
            val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
            if len(trips_list) < 2:
                return trips_list[0][0]
            for i in range(len(trips_list)):
                flag = False
                if i >= 1:
                    pair_first_val, pair_second_val = trips_list[i - 1][0][-1], trips_list[i][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1:
                        flag = True
                if i <= len(trips_list) - 2:
                    pair_first_val, pair_second_val = trips_list[i][0][-1], trips_list[i + 1][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1:
                        flag = True
                if trips_list[i][0][-1] == 'T':
                    flag_T, flag_J, flag_Q = flag_TJQ(trips_list_from_handcards)
                    if flag_J:
                        flag = True
                if flag:
                    continue
                else:
                    return trips_list[i][0]
            return trips_list[0][0]

        def choose_in_bomb(bomb_list, bomb_info) -> str:
            def get_card_from_bomb(bomb_list, key):
                for bomb in bomb_list:
                    for card in bomb:
                        if card[-1] == key:
                            return card

            for key, value in bomb_info:
                if value > 4:
                    return get_card_from_bomb(bomb_list, key)
            return bomb_list[0][0]

        combined_handcards, handCards_bomb_info = combine_handcards(handCards, rank, card_val)  

        combined_temp = {"Single": [], "Trips": [], "Pair": [], "Bomb": []}
        temp_bomb_info = {}
        for card in combined_handcards["Single"]:
            if card_val[card[-1]] <= 10:
                combined_temp["Single"].append(card)
        for trips_card in combined_handcards["Trips"]:
            if card_val[trips_card[0][-1]] <= 10:
                combined_temp["Trips"].append(trips_card)
        for pair_card in combined_handcards["Pair"]:
            if card_val[pair_card[0][-1]] <= 10:
                combined_temp["Pair"].append(pair_card)
        for bomb_card in combined_handcards["Bomb"]:
            if card_val[bomb_card[0][-1]] <= 10:
                combined_temp["Bomb"].append(bomb_card)
        for key, values in handCards_bomb_info.items():
            if card_val[key] <= 10:
                temp_bomb_info[key] = values

        card = None
        if combined_temp["Single"]:
            
            card = choose_in_single(combined_temp["Single"])
        elif combined_temp["Trips"]:
            
            card = choose_in_trips(combined_temp["Trips"], combined_handcards["Trips"])
        elif combined_temp["Pair"]:
            
            card = choose_in_pair(combined_temp["Pair"], combined_handcards["Pair"])
        elif combined_temp["Bomb"]:
            
            card = choose_in_bomb(combined_temp["Bomb"], temp_bomb_info)
        else:
            
            temp = []  
            for handCard in handCards:
                if card_val[handCard[-1]] <= 10:
                    temp.append(handCard)
            card = temp[randint(0, len(temp) - 1)]
        return get_card_index(card)

    def tribute(self,actionList,rank):
        rank_card = 'H'+rank
        first_action = actionList[0]
        if rank_card in first_action[2]:
            return 1
        else:
            return 0


class MyClient(WebSocketClient):
    def __init__(self, url, args, unknown_args):
        super().__init__(url)
        self.state = State()
        self.player = Player(args, unknown_args)
        self.args = args
        self.history_action = {0: [], 1: [], 2: [], 3:[]}
        self.action_seq = []
        self.other_left_hands = [2 for _ in range(54)]
        self.flag = 0

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        # 先序列化收到的消息，转为Python中的字典
        message = json.loads(str(message))

        # 调用状态对象来解析状态
        self.state.parse(message)
        
        # 手牌初始化
        if message['stage'] == 'play' and message['type'] == 'notify':
            if message['curPos'] != self.args.client_index:
                self.action_seq.append(card2num(message['curAction'][2]))

        # 需要做动作
        if message["type"] == 'act':
            # 进还贡
            if message["stage"] == "back":
                act_index = self.player.back_action(message, self.state._myPos, self.state.tribute_result)
                self.send(json.dumps({"actIndex": int(act_index)}))
                # 调整手牌
            elif message["stage"] == "tribute":
                act_index = self.player.tribute(message['actionList'], message["curRank"])
                self.send(json.dumps({"actIndex": int(act_index)}))
                # 调整手牌
            # 打牌
            elif message["stage"] == 'play':
                if self.flag == 0:       # 总共牌减去初始手牌
                    init_hand = card2num(message['handCards'])
                    for ele in init_hand:
                        self.other_left_hands[ele] -= 1
                    self.flag = 1
                # 记录history
                for i in range(4):
                    if i == self.args.client_index:
                        print(self.args.client_index,message['publicInfo'])
                    if i != self.args.client_index:
                        if not message['publicInfo'][i]['playArea']:
                            if len(self.action_seq) >= 4 and len(self.action_seq[-1]) == 0 and len(self.action_seq[-2]) == 0:
                                self.history_action[i].append([])
                        else:
                            action = card2num(message['publicInfo'][i]['playArea'][2])
                            self.history_action[i].append(action)
                            for ele in action:
                                self.other_left_hands[ele] -= 1
                # 做动作
                state = self.prepare(message)
                act_index = self.player.play(state)
                self.action_seq.append(card2num(message['actionList'][act_index][2]))
                self.send(json.dumps({"actIndex": int(act_index)}))

        # 小局结束，传输数据到learner端
        if message['stage'] == 'episodeOver':
            reward = self.get_reward(message)
            self.player.send_data(reward)
            self.history_action = {0: [], 1: [], 2: [], 3:[]}
            self.action_seq = []
            self.other_left_hands = [2 for _ in range(54)]
            self.flag = 0

    def get_reward(self, message):
        team = [self.args.client_index, (self.args.client_index + 2) % 4]
        order = message['order']
        rewards = {"1100": 3, "1010": 2, "1001": 1, "0110": -1, "0101": -2, "0011": -3}
        res = ""
        for i in order:
            if i in team:
                res += '1'
            else:
                res += '0'
        return rewards[res]

    def prepare(self, message):
        num_legal_actions = message['indexRange'] + 1
        legal_actions = [card2num(i[2]) for i in message['actionList']]
        my_handcards = card2array(card2num(message['handCards']))   # 自己的手牌,54维
        my_handcards_batch = np.repeat(my_handcards[np.newaxis, :],
                                   num_legal_actions, axis=0)

        other_hands = []       # 其余所有玩家手上剩余的牌，54维
        for i in range(54): 
            if self.other_left_hands[i] == 1:
                other_hands.append(i)
            elif self.other_left_hands[i] == 2:
                other_hands.append(i)
                other_hands.append(i)
        other_handcards = card2array(other_hands)      
        other_handcards_batch = np.repeat(other_handcards[np.newaxis, :],
                                      num_legal_actions, axis=0)

        last_action = []         # 上家的动作，54维
        if len(self.action_seq) > 0:
            last_action = card2array(self.action_seq[-1])
        else:
            last_action = card2array([])
        last_action_batch = np.repeat(last_action[np.newaxis, :],
                                  num_legal_actions, axis=0)
        
        last_teammate_action = []
        if len(self.history_action[(self.args.client_index + 2) % 4]) > 0 :
            last_teammate_action = card2array(self.history_action[(self.args.client_index + 2) % 4][-1])
        else:
            last_teammate_action = card2array([])
        last_teammate_action_batch = np.repeat(last_teammate_action[np.newaxis, :], num_legal_actions, axis=0)

        my_action_batch = np.zeros(my_handcards_batch.shape)     # 合法动作，54维
        for j, action in enumerate(legal_actions):
            my_action_batch[j, :] = card2array(action)

        down_num_cards_left = _get_one_hot_array(message['publicInfo'][(self.args.client_index + 1) % 4]['rest'], 27)   # 下家剩余的牌数， 27维
        down_num_cards_left_batch = np.repeat(down_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        teammate_num_cards_left = _get_one_hot_array(message['publicInfo'][(self.args.client_index + 2) % 4]['rest'], 27)   # 对家剩余的牌数
        teammate_num_cards_left_batch = np.repeat(teammate_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        up_num_cards_left = _get_one_hot_array(message['publicInfo'][(self.args.client_index + 3) % 4]['rest'], 27)   # 上家剩余的牌数
        up_num_cards_left_batch = np.repeat(up_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.args.client_index + 1) % 4]) > 0:
            down_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.args.client_index + 1) % 4]))    # 下家打过的牌， 54维
        else:
            down_played_cards = card2array([])
        down_played_cards_batch = np.repeat(down_played_cards[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.args.client_index + 2) % 4]) > 0:
            teammate_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.args.client_index + 2) % 4]))    # 对家打过的牌
        else:
            teammate_played_cards = card2array([])
        teammate_played_cards_batch = np.repeat(teammate_played_cards[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.args.client_index + 3) % 4]) > 0:
            up_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.args.client_index + 3) % 4]))    # 上家打过的牌
        else:
            up_played_cards = card2array([])
        up_played_cards_batch = np.repeat(up_played_cards[np.newaxis, :], num_legal_actions, axis=0)
 
        self_rank = _get_one_hot_array(RANK[message['selfRank']], 13)         # 己方当前的级牌，13维
        self_rank_batch = np.repeat(self_rank[np.newaxis, :], num_legal_actions, axis=0)

        oppo_rank = _get_one_hot_array(RANK[message['oppoRank']], 13)         # 敌方当前的级牌
        oppo_rank_batch = np.repeat(oppo_rank[np.newaxis, :], num_legal_actions, axis=0)

        cur_rank = _get_one_hot_array(RANK[message['curRank']], 13)         # 当前的级牌
        cur_rank_batch = np.repeat(cur_rank[np.newaxis, :], num_legal_actions, axis=0)

        x_batch = np.hstack((my_handcards_batch,
                        other_handcards_batch,
                        last_action_batch,
                        last_teammate_action_batch,
                        down_played_cards_batch,
                        teammate_played_cards_batch,
                        up_played_cards_batch,
                        down_num_cards_left_batch,
                        teammate_num_cards_left_batch,
                        up_num_cards_left_batch,
                        self_rank_batch,
                        oppo_rank_batch,
                        cur_rank_batch,
                        my_action_batch))
        x_no_action = np.hstack((my_handcards,
                            other_handcards,
                            last_action,
                            last_teammate_action,
                            down_played_cards,
                            teammate_played_cards,
                            up_played_cards,
                            down_num_cards_left,
                            teammate_num_cards_left,
                            up_num_cards_left,
                            self_rank,
                            oppo_rank,
                            cur_rank))
        z = _action_seq_list2array(_process_action_seq(self.action_seq))
        z_batch = np.repeat(z[np.newaxis, :, :], num_legal_actions, axis=0)

        obs = {
            'x_batch': x_batch.astype(np.float32),
            'z_batch': z_batch.astype(np.float32),
            'legal_actions': legal_actions,
            'x_no_action': x_no_action.astype(np.int8),
            'z': z.astype(np.int8),
          }
        return obs


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cilent_index', type=int, default=3,
                    help='The YAML configuration file')
    args, unknown_args = parser.parse_known_args()
    list = {'type': 'act', 'stage': 'play', 'handCards': ['S2', 'D2', 'C3', 'S4', 'C4', 'D4', 'S5', 'H5', 'C6', 'D6', 'C7', 'D7', 'H8', 'D8', 'H9', 'C9', 'C9', 'DT', 'CJ', 'DJ', 'HQ', 'CQ', 'SK', 'CA', 'DA', 'DA', 'SB'], 'publicInfo': [{'rest': 0, 'playArea': ['Single', 'T', ['ST']]}, {'rest': 0, 'playArea': ['Single', '4', ['H4']]}, {'rest': 1, 'playArea': ['Single', 'Q', ['SQ']]}, {'rest': 27, 'playArea': [None, None, None]}], 'selfRank': '4', 'oppoRank': 'A', 'curRank': 'A', 'curPos': 2, 'curAction': ['Single', 'Q', ['SQ']], 'greaterPos': 2, 'greaterAction': ['Single', 'Q', ['SQ']], 'actionList': [['PASS', 'PASS', 'PASS'], ['Single', 'K', ['SK']], ['Single', 'A', ['CA']], ['Single', 'A', ['DA']], ['Single', 'B', ['SB']]], 'indexRange': 4}
    agent = MyClient(f'ws://127.0.0.1:9618/game/gd/client3', args, unknown_args)
    obs = agent.prepare(list)
    print(obs)
