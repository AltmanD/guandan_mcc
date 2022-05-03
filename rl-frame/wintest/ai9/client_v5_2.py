# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:


import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from action import Action

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Util2 import *

class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = Action()
        self.action_team = ACTIONTEAM()
        self.action_first = ACTIONFIRST()
        self.action_enemy = ACTIONENEMY()
        self.myPos = -1
        self.cardRecorder = {'2':{'S':4, 'H':4, 'C':4, 'D':4},
                '3': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '4': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '5': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '6': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '7': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '8': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                '9': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'T': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'J': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'Q': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'K': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'A': {'S': 4, 'H': 4, 'C': 4, 'D': 4},
                'B': {'S': 2},
                'R': {'H': 2}}

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def get_single(self, message, card_type = 'Pair'):
        Universal = 'H' + message['curRank']
        action_list = message["actionList"]
        ignoreList = []
        for i in range(len(action_list)):
            type, cur_rank, cur_action = action_list[i]
            if Universal in cur_action and len(cur_action) > 1:
                ignoreList.append(i)
        cardList = []
        for i in range(len(action_list)):
            type, cur_rank, cur_action = action_list[i]
            if type == card_type and i not in ignoreList:
                count = 0
                for j in action_list[i+1:]:
                    _type, _cur_rank, _cur_action = j
                    if _cur_rank in ['B','R']:
                        continue
                    if cur_rank == _cur_rank and Universal not in _cur_action:
                        count += 1
                if count < 1:
                    cardList.append({'index':i, 'rank':cur_rank, 'action':cur_action})
        return cardList

    def get_pairtrips(self, message, card_type = 'Pair'):
        Universal = 'H' + message['curRank']
        action_list = message["actionList"]
        cardIndexList, cardRankList, cardActionList = [], [], []
        for i in range(len(action_list)):
            type, cur_rank, cur_action = action_list[i]
            if type == card_type and Universal not in cur_action:
                cardIndexList.append(i)
                cardRankList.append(cur_rank)
                cardActionList.append(cur_action)
        cardList = []
        for i in range(len(cardRankList)):
            count = cardRankList.count(cardRankList[i])
            if count > 1 or cardRankList[i] in ['B','R']: #
                continue
            else:
                cardList.append({'index':cardIndexList[i], 'rank':cardRankList[i], 'action':cardActionList[i]})
        return cardList

    def get_card_type(self, message):
        action_list = message["actionList"]
        cardTypeList = {'TwoTrips': [], 'ThreePair': [], 'Straight': [], 'ThreeWithTwo': [], 'Pair': [], 'Single': [],
                      'Trips': [], 'Bomb': [], 'StraightFlush': [], 'PASS':[], 'tribute':[], 'back':[]}
        if len(action_list) < 2:
            for i in range(len(action_list)):
                type, cur_rank, cur_action = action_list[i]
                cardTypeList[type].append({'index':i, 'rank':cur_rank, 'action':cur_action})
            return cardTypeList

        for i in range(len(action_list)):
            type, cur_rank, cur_action = action_list[i]
            if cur_action == 'PASS':
                cardTypeList[type].append({'index':i, 'rank':cur_rank, 'action':cur_action})
            elif len(cur_action) > 3:
                cardTypeList[type].append({'index':i, 'rank':cur_rank, 'action':cur_action})

        cardTypeList['Single'] = self.get_single(message, card_type='Single')
        cardTypeList['Pair'] = self.get_pairtrips(message, card_type='Pair')
        cardTypeList['Trips'] = self.get_pairtrips(message, card_type='Trips')
        return cardTypeList

    def get_bombCards(self, message):
        # 不拆炸弹用到的牌
        Universal = 'H' + message['curRank']
        bombCardsLists = {'StraightFlush': [], 'Bomb': []}
        bombList = ['StraightFlush', 'Bomb']
        for i in bombList:
            bombCardsList = []
            for j in message['actionList']:
                cur_card_type, cur_rank, cur_action = j
                if i != cur_card_type:
                    continue
                else:
                    for k in cur_action:
                        bombCardsList.append(k)
            set(bombCardsList)  # 去重
            bombCardsLists[i] = bombCardsList
        return bombCardsLists

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                             # 调用状态对象来解析状态

        if self.myPos < 0:
            self.myPos = message['myPos']
        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            bombCardsLists = self.get_bombCards(message)
            cardTypeList = self.get_card_type(message)

            if 'PASS' in message['actionList'][0]:
                if self.action_team.bool_action_team(message, self.myPos):
                    act_index = self.action_team.ActionTeam(message, bombCardsLists, cardTypeList, fuckRank = 10)
                else:
                    act_index = self.action_enemy.ActionEnemy(message, bombCardsLists, cardTypeList, self.myPos)
            else:
                act_index = self.action_first.ActionFirst(message, bombCardsLists, cardTypeList, WarningCard=10)
            actionListIndex = []
            for i in range(len(message['actionList'])):
                actionListIndex.append(i)
            if act_index not in actionListIndex:
                act_index = 0
            print('myPos', self.myPos)

            self.send(json.dumps({"actIndex": act_index}))
        # elif message['stage'] == 'beginning':
        #     handCards = message['handCards']
        #     for i in handCards:
        #         decor, rank = list(i)
        #         cardRecorder[rank][decor] -= 1
        # elif message['stage'] != 'episodeOver':
        #     print('message', message)
        #     if 'PASS'not in message['curAction']:
        #         _, _, action = message['curAction']
        #         for i in action:
        #             decor, rank = list(i)
        #             cardRecorder[rank][decor] -= 1

if __name__ == '__main__':
    try: #'ws://39.108.189.48:80/game/gd/15961703636871692'
        ws = ExampleClient('ws://127.0.0.1:23456/game/client2')
        # ws = ExampleClient('ws://120.27.241.20:80/game/gd/15961703636299687')
        # ws = ExampleClient('ws://39.108.189.48:80/game/gd/13811449933406988')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
