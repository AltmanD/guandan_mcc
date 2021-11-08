# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类

from random import randint

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

    def GetIndexFromBack(self, msg, retValue): #"actionList": [['back', 'back', ['S2']], ['back', 'back', ['H2']]
        retIndex = 0
        print("retValue:", retValue)
        retAction = retValue['action']
        for action in msg["actionList"]:
            if (action[2] == retAction):
                retIndex = msg["actionList"].index(action)
        print("选择动作：", retIndex, "动作为：", msg["actionList"][retIndex])
        return retIndex

    def GetIndexFromPlay(self, msg, retValue):
        #print("actionlist:",msg["actionList"])

        sortedAction = retValue["action"]
        if retValue["type"] != "PASS":
            sortedAction.sort()
        print("retValue:",retValue)
        retIndex = 0
        for action in msg["actionList"]:
            if (action[2]!="PASS"): action[2].sort()
            #print("retvalue:",retValue["type"], retValue["rank"], sortedAction)
            #print("actionfromlist:",action[0], action[1], action[2])
            if (action[0]==retValue["type"] and action[1]==retValue["rank"] and action[2]==sortedAction):
                retIndex=msg["actionList"].index(action)
        print("选择动作：", retIndex, "动作为：", msg["actionList"][retIndex])
        return retIndex

    def parse(self, msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        print(self.action)
        print("可选动作范围为：0至{}".format(self.act_range))
        return randint(0, self.act_range)
