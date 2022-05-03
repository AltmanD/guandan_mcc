# -*- coding: utf-8 -*-
# @Time       : 12020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类

import copy
import logging
from random import randint, random

from active import *
from passive import *
from utils.utils import *

# 中英文对照表
ENG2CH = {
    "Single": "单张",
    "Pair": "对子",
    "Trips": "三张",
    "ThreePair": "三连对",
    "ThreeWithTwo": "三带二",
    "TwoTrips": "钢板",
    "Straight": "顺子",
    "StraightFlush": "同花顺",
    "Bomb": "炸弹",
    "PASS": "过"
}
from back_tribute import *


class Action(object):

    def __init__(self):
        self.action = []
        self.act_range = -1

    def rule_parse(self,msg,mypos,remaincards,history,remain_cards_classbynum,pass_num,my_pass_num,tribute_result):
        self.action = msg["actionList"]
        if len(self.action) == 1:
            return 0
        if msg["stage"] == "play" and msg["greaterPos"] != mypos and msg["curPos"] != -1:
            try:

                numofplayers = [history['0']["remain"],history['1']["remain"],history['2']["remain"],history['3']["remain"]]
                numofnext = numofplayers[(mypos + 1) % 4]
                if numofnext != 0:
                    print("下家还有{}张牌".format(numofnext))
                else:
                    numofpre = numofplayers[(mypos - 1) % 4]
                    print("下家已完牌，上家还有{}张牌".format(numofpre))
                self.act = passive(self.action, msg["handCards"], msg["curRank"], msg['curAction'],msg["greaterAction"],mypos,
                                        msg["greaterPos"],remaincards, numofplayers,pass_num,my_pass_num,remain_cards_classbynum)
            except Exception as e:
                print(str(e))
                self.act = 1

        elif msg["stage"] == "play" and (msg["greaterPos"] == -1 or msg["curPos"] == -1):
            print("主动出牌")
            try:
                numofplayers = [history['0']["remain"], history['1']["remain"], history['2']["remain"],
                                history['3']["remain"]]
                numofnext = numofplayers[(mypos + 1) % 4]
                if numofnext != 0:
                    print("下家还有{}张牌".format(numofnext))
                else:
                    numofpre = numofplayers[(mypos - 1) % 4]
                    print("下家已完牌，上家还有{}张牌".format(numofpre))
                self.act = active(self.action, msg["handCards"], msg["curRank"],numofplayers,mypos,remaincards)
            except Exception as e:
                print(e)
                self.act = 0
        elif msg["stage"] == "back":
            try:
                self.act = back_action(msg,mypos,tribute_result)
            except Exception as e:
                print(e)
                self.act = 0
        elif msg["stage"] == "tribute":
            try:
                self.act = tribute(self.action,msg["curRank"])
            except Exception as e:
                print(e)
                self.act = 0
        else:
            self.act_range = msg["indexRange"]
            self.act = randint(0, self.act_range)
        try:
            if self.action[self.act][0]=="PASS":
                print("当我过的时候我可以选择哪些牌：")
                print(self.action)
        except Exception as e:
            print("日志打印失败")
            print(e)
        return self.act

    def random_parse(self,msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        return randint(0,self.act_range)

    