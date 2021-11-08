# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类
# 版本号：INDEX OS2.0.0

from random import randint
from message_Reyn_CUR import check_message

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


class Action(object):

    def __init__(self):
        self.action = []
        self.act_range = -1
        self.AI_choice = -1

    #该为完全随机数的行动
    def parse(self, msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        print(self.action)
        print("可选动作范围为：0至{}".format(self.act_range))
        return randint(0, self.act_range)

    #该为有AI加持的确定行动
    def parse_AI(self, msg, pos):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        print(self.action)
        #运行AI来确定需要出的牌
        self.AI_choice = check_message(msg,pos)
        #由于没有考虑进贡，故而随机，否则bug
        if self.AI_choice == None:
            return randint(0, self.act_range)
        print("AI选择的出牌编号为:{}".format(self.AI_choice))
        return self.AI_choice