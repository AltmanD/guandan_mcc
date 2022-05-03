# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类

from random import randint
from Myfunc1014 import Myfunc1014
from lasthand import lasthand
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
        self.myfunc1014 = Myfunc1014()
        self.lasthand = lasthand()

    def parse(self, msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        with open('data4.txt') as file_obj:
            content = file_obj.read()
        rest_card = []
        for i in range(0, 4):
            rest_card.append(msg['publicInfo'][i]['rest'])
        myclient = int(content)
        under6_tot = self.myfunc1014.under6_total(rest_card) #剩余手牌数小于6的人的个数
        rest_cardmin_index = rest_card.index(min(rest_card))  # 最小剩余的手牌人的索引
        secondmin = self.myfunc1014.secondmin2(rest_card)  # 剩余手牌第二小的人的数
        secondmin_index = rest_card.index(secondmin) # 剩余手牌第二小的人的数的索引
        thirdmin = self.myfunc1014.thirdmin(rest_card)  # 剩余手牌第三小的人的数
        thirdmin_index = rest_card.index(thirdmin)  # 剩余手牌第三小的人的数的索引
        forthmin = self.myfunc1014.forthmin(rest_card)  # 剩余手牌第四个小的人的数
        forthmin_index = rest_card.index(forthmin)  # 剩余手牌第四小的人的数的索引
        print("可选动作范围为：0至{}".format(self.act_range))
        #最新配牌出牌策略
        print("这里会反映每个msg",msg)
        if msg['stage']=='back':#还贡
            print("还贡操作",msg)
            hmfunfircard0 = self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[0]
            hmfunfircard1 = self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[1]
            hmfunfircardSingle = self.myfunc1014.lgetcard(hmfunfircard0,hmfunfircard1)['Single']
            hmfunfircardPair = self.myfunc1014.lgetcard(hmfunfircard0,hmfunfircard1)['Pair']
            if hmfunfircardSingle != []:
                cards = self.myfunc1014.search_color(msg['handCards'], hmfunfircardSingle[0])
                gettion_index1 = self.myfunc1014.getindex(msg['actionList'],cards)
                return gettion_index1
            elif hmfunfircardPair != []:
                cards = self.myfunc1014.search_color(msg['handCards'],hmfunfircardPair[0])
                gettion_index1 = self.myfunc1014.getindex(msg['actionList'], cards)
                return gettion_index1
            else:
                return 0
        elif (msg['greaterPos'] == -1) and msg['stage'] == 'play':#这是先手出牌
            print("我先手的msg",msg)
            xmfunfircard0 = self.myfunc1014.firstcard(msg['handCards'],msg['curRank'])[0]
            xmfunfircard1 = self.myfunc1014.firstcard(msg['handCards'],msg['curRank'])[1]
            xmfunlgetcard = self.myfunc1014.lgetcard(xmfunfircard0,xmfunfircard1)
            xgetcolor = self.myfunc1014.getcolor(xmfunlgetcard, msg['curRank'])
            if min(rest_card) > 6:
                gettion_index1 = self.myfunc1014.getindex(msg['actionList'],xgetcolor)
                print("这是先手的gettion_index1",gettion_index1)
                if gettion_index1 == None:
                    return 0
                else:
                    return gettion_index1
            else:
                if under6_tot == 1 and rest_cardmin_index % 2 != myclient % 2 and min(rest_card) == 1:
                    #如果手牌数小于6的个数为1 且不是我的对家，手牌数为1  不优先出单张
                    typec = 'Single'
                    msg2 = self.myfunc1014.lgetcard(xmfunfircard0,xmfunfircard1)
                    if msg2['ThreeWithTwo'] == [] and msg2['Pair'] == [] and msg2['Trips'] == [] and msg2[
                        'ThreePair'] == [] and msg2['ThreePair'] == [] and msg2['Straight'] == [] and msg2[
                        'Bomb'] == [] and msg2['StraightFlush'] == []:
                        #这边看一下
                        gettion_index1 = self.myfunc1014.getindex(msg['actionList'], xgetcolor)
                        if gettion_index1 == None:
                            return 0
                        else:
                            return gettion_index1
                    else:
                        print("我调用了")
                        # gettion_index1 = self.myfunc1014.getindex(msg['actionList'], self.myfunc1014.getcolor2(msg2, msg['curRank'], typec))
                        gettion_index1 = self.myfunc1014.getindex(msg['actionList'], self.myfunc1014.getcolor2(
                            self.myfunc1014.lgetcard(self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[0],
                                                     self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[1]),
                            msg['curRank'],typec))
                        if gettion_index1 == None:
                            return 0
                        else:
                            return gettion_index1
                elif under6_tot == 1 and rest_cardmin_index % 2 != myclient % 2 and min(rest_card) == 2:
                    # 如果手牌数小于6的个数为1 且不是我的对家，手牌数为2  不优先出对子
                    typec = 'Pair'
                    msg2 = self.myfunc1014.lgetcard(xmfunfircard0,xmfunfircard1)
                    if msg2['ThreeWithTwo'] == [] and msg2['Single'] == [] and msg2['Trips'] == [] and msg2[
                        'ThreePair'] == [] and msg2['ThreePair'] == [] and msg2['Straight'] == [] and msg2[
                        'Bomb'] == [] and msg2['StraightFlush'] == []:
                        xgetcolor = self.myfunc1014.getcolor(xmfunlgetcard, msg['curRank'])
                        gettion_index1 = self.myfunc1014.getindex(msg['actionList'], xgetcolor)
                        if gettion_index1 == None:
                            return 0
                        else:
                            return gettion_index1
                    else:
                        print("我调用了")
                        # gettion_index1 = self.myfunc1014.getindex(msg['actionList'],self.myfunc1014.getcolor2(msg2, msg['curRank'],typec))
                        gettion_index1 = self.myfunc1014.getindex(msg['actionList'], self.myfunc1014.getcolor2(self.myfunc1014.lgetcard(self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[0],self.myfunc1014.firstcard(msg['handCards'], msg['curRank'])[1]),msg['curRank'],typec))
                        if gettion_index1 == None:
                            return 0
                        else:
                            return gettion_index1
                else:
                    gettion_index1 = self.myfunc1014.getindex(msg['actionList'], xgetcolor)
                    if gettion_index1 == None:
                        return 0
                    else:
                        return gettion_index1
        if(msg['greaterPos'] != -1): #后手
            lastfircard0 = self.lasthand.firstcard(msg['handCards'], msg['curRank'])[0]
            lastfircard1 = self.lasthand.firstcard(msg['handCards'], msg['curRank'])[1]
            dict1 = self.lasthand.hgetcard(lastfircard0,lastfircard1, msg['curRank'])
            lastgetBomb = self.lasthand.getBomb(msg['greaterAction'], dict1,msg['curRank'])
            reSort21 = self.myfunc1014.reSort2(msg['curRank'], msg['greaterAction'][1])
            reSort9 = self.myfunc1014.reSortun9(msg['curRank'], msg['greaterAction'][1])
            reSortQ = self.myfunc1014.reSortunQ(msg['curRank'], msg['greaterAction'][1])
            lastgetcolor =  self.lasthand.getcolor(dict1, msg['curRank'], msg['greaterAction'])
            print("这是dict1",dict1)
            if self.lasthand.getlen(dict1) == 1 and (myclient % 2 != int(msg['greaterPos']) % 2):
                print("我炸弹多")
                getBomb_index = self.lasthand.getindex(msg['actionList'],lastgetBomb)
                return getBomb_index
            elif (myclient % 2 == int(msg['greaterPos']) % 2 and reSort21):
                #最大出牌是对家且最大出牌类型是炸弹，或者最大出牌数值是大于A的情况，直接pass
                return 0
            elif (myclient % 2 == int(msg['greaterPos']) % 2 and msg['greaterAction'][0]=="Bomb"):
                return 0
            elif (myclient % 2 == int(msg['greaterPos']) % 2 and msg['greaterAction'][0]=="ThreeWithTwo" and reSort9):
                #如果出牌是对家且最大出牌类型是三连对，且出牌是大于9的情况，不压牌
                return 0
            elif (myclient % 2 == int(msg['greaterPos']) % 2 and msg['greaterAction'][0]=="TwoTrips" and reSort9):
                #如果出牌的是对家且最大出牌类型是钢板，且出牌大于9的情况，不压牌
                return 0
            elif (myclient % 2 == int(msg['greaterPos']) % 2 and msg['greaterAction'][0]=="TwoTrips" and reSortQ):
                #如果出牌是对家且最大出牌类型是三代二，且出牌大于Q的情况，不压牌
                return 0
            else:
                if min(rest_card) > 6: #如果剩余手牌数大于6张的情况
                    print("剩余手牌数大于6张")
                    gettion_index1 = self.lasthand.getindex(msg['actionList'], lastgetcolor)
                    print("这是后手msg手牌", msg['handCards'])
                    if gettion_index1 == 0:
                        return 0
                    elif gettion_index1 == None:
                        return 0
                    else:
                        return gettion_index1
                else:#如果剩余手牌数小于6张的情况
                    clientshang = self.lasthand.client_shang(myclient)
                    clientxia = self.lasthand.client_xia(myclient)
                    reSort31 = self.myfunc1014.reSort3(msg['curRank'], msg['greaterAction'][1])
                    if rest_card[clientxia] == 1 and msg['greaterAction'][0] == 'Single' and reSort31:
                    # 如果下家有1张，且最大手牌出的单张，且小于A，优先用最大的单张压 如果index为0的情况？ 调用出炸弹的函数
                        print("情况1")
                        if len(dict1['Single']) != 0:
                            gettion_index1 = self.lasthand.getindex(msg['actionList'],dict1['Single'][-1])
                            if gettion_index1 == 0:
                                return 0
                            else:
                                return gettion_index1
                        else:
                            #返回炸弹
                            print("成都")
                            getBomb_index = self.lasthand.getindex(msg['actionList'], lastgetBomb)
                            return getBomb_index
                    elif rest_card[clientxia] == 2 and msg['greaterAction'][0] == 'Pair' and reSort31:
                        #如果下家有2张，且最大手牌出的对子，且小于A，优先出最大的对子 ，如果index为0的情况？调用出炸弹的函数
                        print("情况2")
                        if len(dict1['Pair']) != 0:
                            gettion_index1 = self.lasthand.getindex(msg['actionList'],dict1['Pair'][-1])
                            if gettion_index1 == 0:
                                #这边改
                                return 0
                            else:
                                return gettion_index1
                        else:
                            # 返回炸弹
                            print("成都")
                            getBomb_index = self.lasthand.getindex(msg['actionList'], lastgetBomb)
                            return getBomb_index
                    else:
                        gettion_index1 = self.lasthand.getindex(msg['actionList'], lastgetcolor)
                        if gettion_index1 == 0 and len(msg['actionList']) > 1 and msg['actionList'][1][0] == 'Bomb' and (myclient % 2 != int(msg['greaterPos']) % 2) and rest_card[rest_cardmin_index] != 4:
                            print("这是后手小于六张，不是对家", rest_cardmin_index)
                            getBomb_index = self.lasthand.getindex(msg['actionList'],lastgetBomb)
                            return getBomb_index
                        elif gettion_index1 == 0:
                            return 0
                        elif gettion_index1 == None:
                            return 0
                        else:
                            return gettion_index1
        else:
            return randint(0, self.act_range)