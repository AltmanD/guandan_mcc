import json
import os
import warnings
from argparse import ArgumentParser
from functools import reduce
from random import randint

import numpy as np
import zmq
from pyarrow import deserialize, serialize
from ws4py.client.threadedclient import WebSocketClient

from util import card2array, card2num, combine_handcards

warnings.filterwarnings("ignore")
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
parser = ArgumentParser()
parser.add_argument('--ip', type=str, default='127.0.0.1',
                    help='IP address of learner server')
parser.add_argument('--action_port', type=int, default=6000,
                    help='Learner server port to send training data')

RANK = {
    '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8,
    'T':9, 'J':10, 'Q':11, 'K':12, 'A':13
}

def _get_one_hot_array(num_left_cards, max_num_cards, flag):
    if flag == 0:     # 级数的情况
        one_hot = np.zeros(max_num_cards)
        one_hot[num_left_cards - 1] = 1
    else:
        one_hot = np.zeros(max_num_cards+1)    # 剩余的牌（0-1阵格式）
        one_hot[num_left_cards] = 1
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

class ExampleClient(WebSocketClient):
    def __init__(self, url, args):
        super().__init__(url)
        self.args = args
        self.mypos = 0
        self.history_action = {0: [], 1: [], 2: [], 3:[]}
        self.action_seq = []
        self.action_order = [] # 记录出牌顺序(4个智能体是一样的)
        self.remaining = {0: 27, 1: 27, 2: 27, 3: 27}
        self.other_left_hands = [2 for _ in range(54)]
        self.flag = 0
        self.over = []
        self.rank = {'self_rank': 1, 'oppo_rank': 1}

        # 初始化zmq
        self.context = zmq.Context()
        self.context.linger = 0 
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f'tcp://localhost:{6003}')

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        # 先序列化收到的消息，转为Python中的字典
        message = json.loads(str(message))
        if message['type'] == 'notify':
            # 牌局开始记录位置
            if message['stage'] == 'beginning':
                self.mypos = message['myPos']
            # 记录进贡的牌
            elif message['stage'] == 'tribute':
                self.tribute_result = message['result']
            # 在动作序列中记录动作
            elif message['stage'] == 'play':
                just_play = message['curPos']
                action = card2num(message['curAction'][2])
                if message['curPos'] != self.mypos:
                    for ele in action:
                        self.other_left_hands[ele] -= 1
                if len(self.over) == 0:    # 如果没人出完牌
                    self.action_order.append(just_play)
                    self.action_seq.append(action)
                    self.history_action[message['curPos']].append(action)
                elif len(self.over) == 1:    # 只有一个出完牌的（如果队友也先赢了，就会直接结束）
                    if len(action) > 0 and self.flag == 1: # 第一轮有人接下来了，则顺序没问题
                        self.flag = 2
                        if just_play == (self.over[0] + 3) % 4:     # 是头游的上家接下来的
                            self.action_order.append(just_play)       
                            self.action_seq.append(action)
                            self.history_action[message['curPos']].append(action)
                            self.action_order.append(self.over[0])      # 添加第一个出完牌的玩家的信息
                            self.history_action[self.over[0]].append([-1])
                            self.action_seq.append([-1])
                            # self.history_action[self.over[0]].append([])
                            # self.action_seq.append([])
                        else:
                            self.action_order.append(just_play)        # 不是头游的上家接的
                            self.action_seq.append(action)
                            self.history_action[message['curPos']].append(action)
                    elif self.flag == 1 and (just_play + 1) % 4 == self.over[0]:      # 出完牌后全都没接的情况，由出完牌的对家出牌（如0、1、2、3、2）
                        self.flag = 2
                        self.action_order.append(just_play)        # 添加出完牌的上家
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)
                        self.action_order.append(self.over[0])      # 添加第一个出完牌的玩家的信息
                        # self.history_action[self.over[0]].append([])
                        # self.action_seq.append([])
                        self.history_action[self.over[0]].append([-1])
                        self.action_seq.append([-1])
                        self.action_order.append((just_play + 2) % 4)      # 添加被跳过出牌的玩家的信息
                        self.history_action[(just_play + 2) % 4].append([])
                        self.action_seq.append([])
                    elif just_play == (self.over[0] + 3) % 4 and self.flag == 2:      # 当第一个出完牌的上家已经出过牌了(过完接风的第一轮后或有人接牌了)
                        self.action_order.append(just_play)        # 继续添加正常的信息
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)
                        self.action_order.append(self.over[0])      # 添加第一个出完牌的玩家的信息
                        # self.history_action[self.over[0]].append([])
                        # self.action_seq.append([])
                        self.history_action[self.over[0]].append([-1])
                        self.action_seq.append([-1])
                    else:
                        self.action_order.append(just_play)        # 继续添加正常的信息
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)
                elif len(self.over) == 2:   # 可能包含两种情形（0、1和1、0出完情况不一样）
                    if len(action) > 0 and self.flag <= 2:           # 有人接下来的情况
                        if (just_play+1) % 4 not in self.over:          # 下家牌没出完时，正常放过去
                            self.flag = 3        
                            self.action_order.append(just_play)        
                            self.action_seq.append(action)
                            self.history_action[message['curPos']].append(action)    
                        else:
                            self.flag = 3
                            self.action_order.append(just_play)        # 是前二游玩家的上家接牌时
                            self.action_seq.append(action)
                            self.history_action[message['curPos']].append(action)
                            self.action_order.append((just_play + 1) % 4)     # 先出完的肯定是紧挨着的上下家
                            # self.history_action[(just_play + 1) % 4].append([])
                            # self.action_seq.append([])
                            self.history_action[(just_play + 1) % 4].append([-1])
                            self.action_seq.append([-1])
                            self.action_order.append((just_play + 2) % 4)     
                            # self.history_action[(just_play + 2) % 4].append([])
                            # self.action_seq.append([])     
                            self.history_action[(just_play + 2) % 4].append([-1])
                            self.action_seq.append([-1])     
                    elif self.flag <= 2 and (just_play+1) % 4 in self.over:     # 接风时全都跳过的情况
                        self.flag = 3
                        self.action_order.append(just_play)        # 添加正常的信息
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)     
                        self.action_order.append((just_play + 1) % 4)     # 先出完的肯定是紧挨着的上下家
                        # self.history_action[(just_play + 1) % 4].append([])
                        # self.action_seq.append([])
                        # self.action_order.append((just_play + 2) % 4)     
                        # self.history_action[(just_play + 2) % 4].append([])
                        # self.action_seq.append([])  
                        self.history_action[(just_play + 1) % 4].append([-1])
                        self.action_seq.append([-1])
                        self.action_order.append((just_play + 2) % 4)     
                        self.history_action[(just_play + 2) % 4].append([-1])
                        self.action_seq.append([-1])  
                        if just_play == (self.over[-1] + 2) % 4:  # 0、1情况 (1、0情况不用再加了)
                            self.action_order.append((just_play + 3) % 4)     
                            self.history_action[(just_play + 3) % 4].append([])
                            self.action_seq.append([])                             
                    elif (just_play+1) % 4 in self.over and self.flag == 3: # 没出完牌的一定是上下家关系，当其中一个的下家出完时，就是两个出完的
                        self.action_order.append(just_play)        # 继续添加正常的信息
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)
                        self.action_order.append((just_play + 1) % 4)     # 先出完的肯定是紧挨着的上下家
                        # self.history_action[(just_play + 1) % 4].append([])
                        # self.action_seq.append([])
                        # self.action_order.append((just_play + 2) % 4)     
                        # self.history_action[(just_play + 2) % 4].append([])
                        # self.action_seq.append([])
                        self.history_action[(just_play + 1) % 4].append([-1])
                        self.action_seq.append([-1])
                        self.action_order.append((just_play + 2) % 4)     
                        self.history_action[(just_play + 2) % 4].append([-1])
                        self.action_seq.append([-1])
                    else:
                        self.action_order.append(just_play)        # 继续添加正常的信息
                        self.action_seq.append(action)
                        self.history_action[message['curPos']].append(action)

                self.remaining[just_play] -= len(action)
                if self.remaining[just_play] == 0:
                    self.over.append(just_play)
            else:
                pass       
        # 需要做动作
        elif message["type"] == 'act':
            # 进还贡
            if message["stage"] == "back":
                act_index = self.back_action(message, self.mypos, self.tribute_result)
                self.send(json.dumps({"actIndex": int(act_index)}))
            elif message["stage"] == "tribute":
                act_index = self.tribute(message['actionList'], message["curRank"])
                self.send(json.dumps({"actIndex": int(act_index)}))
            # 打牌
            elif message["stage"] == 'play':
                if self.flag == 0:       # 总共牌减去初始手牌
                    init_hand = card2num(message['handCards'])
                    for ele in init_hand:
                        self.other_left_hands[ele] -= 1
                    self.flag = 1

                # 准备状态数据
                if len(message['actionList']) == 1:
                    self.send(json.dumps({"actIndex": 0}))
                else :
                    state = self.prepare(message)
                    # 传输给决策模块
                    self.socket.send(serialize(state).to_buffer())
                    # 收到决策
                    act_index = deserialize(self.socket.recv())
                    # 作出决策
                    # doaction = message['actionList'][int(act_index)]
                    # print(f'Client{self.mypos} do action{act_index}:{doaction}')
                    self.send(json.dumps({"actIndex": int(act_index)}))

        # 小局结束，数据重置
        if message['stage'] == 'episodeOver':
            self.history_action = {0: [], 1: [], 2: [], 3:[]}
            self.action_seq = []
            self.other_left_hands = [2 for _ in range(54)]
            self.flag = 0
            self.action_order = []
            self.remaining = {0: 27, 1: 27, 2: 27, 3: 27}
            self.over = []

        # 全部打完
        if message['stage'] == 'gameResult' and message['type'] == 'notify':
            print('------------------对局结束-------------------')
            print('胜局统计', message['victoryNum'])
            print('------------------对局结束-------------------')

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
        #print(self.args.client_index, "other handcards: ", other_hands)
        other_handcards = card2array(other_hands)      
        other_handcards_batch = np.repeat(other_handcards[np.newaxis, :],
                                      num_legal_actions, axis=0)

        last_action = []         # 最新的动作，54维
        if len(self.action_seq) > 0:
            last_action = card2array(self.action_seq[-1])
        else:
            last_action = card2array([])
        last_action_batch = np.repeat(last_action[np.newaxis, :],
                                  num_legal_actions, axis=0)
        
        last_teammate_action = []               # 队友最后的动作， 54维
        if len(self.history_action[(self.mypos + 2) % 4]) > 0 :
            last_teammate_action = card2array(self.history_action[(self.mypos + 2) % 4][-1])
        else:
            last_teammate_action = card2array([])
        last_teammate_action_batch = np.repeat(last_teammate_action[np.newaxis, :], num_legal_actions, axis=0)

        my_action_batch = np.zeros(my_handcards_batch.shape)     # 合法动作，54维
        for j, action in enumerate(legal_actions):
            my_action_batch[j, :] = card2array(action)

        down_num_cards_left = _get_one_hot_array(self.remaining[(self.mypos + 1) % 4], 27, 1)   # 下家剩余的牌数， 28维
        down_num_cards_left_batch = np.repeat(down_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        teammate_num_cards_left = _get_one_hot_array(self.remaining[(self.mypos + 2) % 4], 27, 1)   # 对家剩余的牌数
        teammate_num_cards_left_batch = np.repeat(teammate_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        up_num_cards_left = _get_one_hot_array(self.remaining[(self.mypos + 3) % 4], 27, 1)   # 上家剩余的牌数
        up_num_cards_left_batch = np.repeat(up_num_cards_left[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.mypos + 1) % 4]) > 0:
            down_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.mypos + 1) % 4]))    # 下家打过的牌， 54维
        else:
            down_played_cards = card2array([])
        down_played_cards_batch = np.repeat(down_played_cards[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.mypos + 2) % 4]) > 0:
            teammate_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.mypos + 2) % 4]))    # 对家打过的牌
        else:
            teammate_played_cards = card2array([])
        teammate_played_cards_batch = np.repeat(teammate_played_cards[np.newaxis, :], num_legal_actions, axis=0)

        if len(self.history_action[(self.mypos + 3) % 4]) > 0:
            up_played_cards = card2array(reduce(lambda x, y: x+y, self.history_action[(self.mypos + 3) % 4]))    # 上家打过的牌
        else:
            up_played_cards = card2array([])
        up_played_cards_batch = np.repeat(up_played_cards[np.newaxis, :], num_legal_actions, axis=0)
 
        self_rank = _get_one_hot_array(RANK[message['selfRank']], 13, 0)         # 己方当前的级牌，13维
        self_rank_batch = np.repeat(self_rank[np.newaxis, :], num_legal_actions, axis=0)

        oppo_rank = _get_one_hot_array(RANK[message['oppoRank']], 13, 0)         # 敌方当前的级牌
        oppo_rank_batch = np.repeat(oppo_rank[np.newaxis, :], num_legal_actions, axis=0)

        cur_rank = _get_one_hot_array(RANK[message['curRank']], 13, 0)         # 当前的级牌
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
            'x_no_action': x_no_action.astype(np.float32),
            'z': z.astype(np.float32),
          }
        return obs

    # 还贡
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

            for key, value in bomb_info.items():
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

    # 进贡
    def tribute(self,actionList,rank):
        rank_card = 'H'+rank
        first_action = actionList[0]
        if rank_card in first_action[2]:
            return 1
        else:
            return 0

if __name__ == '__main__':
    args, _ = parser.parse_known_args()
    args.client_index = 3
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client3', args)
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
