# -*- coding: utf-8 -*-
# @Time       : 2020/10/19 19:30
# @Author     : Duofeng Wu  &&  Zenghui Qian
# @File       : action.py
# @Description: 动作类

from random import randint
from mysolve import solve
from test import tsolve
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

    def parse(self, msg, mate_pos):     # 增加了一个新参数mate_pos，表示队友的位置
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        print(self.action)
        print("可选动作范围为：0至{}".format(self.act_range))
        index = solve(msg, mate_pos)
        return index
