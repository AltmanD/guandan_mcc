from CreateActionList import CreateActionList
from CountValue import CountValue
from config import CompareRank
import config
import json
import time
from strategy import Strategy


class PlayCard():

    def actBack(self, handCards, curRank):
        bestPlay = []
        maxValue = -100
        for rank in config.cardRanks:
            if (rank!=curRank and rank<='9' and rank>='2'):
                for card in handCards:
                    if (card[1]==rank):
                        action = [card]
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                        if (restValue>maxValue):
                            maxValue = restValue
                            bestPlay = {"action": action, "type": "back", "rank": rank}
                        #print(card, restValue)
                        break
        return bestPlay

    def GetAdditionalActionList(self, typeList, curRank, fullActionList):
        additionalActionList=[]
        dict = {}
        for action in fullActionList:
            if (action[0] in typeList and ((action[0], action[1]) not in dict.keys())):
                for card in action[2]:
                    if card == 'H'+curRank:
                        additionalActionList.append(action)
                        dict[(action[0], action[1])] = 1
                        break
        return additionalActionList

    def FreePlay(self, handCards, curRank, fullActionList = None):
        print("Free play handCards:", handCards, "   restHandsCount:", Strategy.restHandsCount)
        handValue, handActions = CountValue().HandCardsValue(handCards, 0, curRank)
        #print(handActions)
        #Strategy.SetBeginning(0)
        Strategy.SetRole(handValue, handActions, curRank)
        Strategy.makeReviseValues()
        #print(Strategy.recordPlayerActions)
        additionalActionList = self.GetAdditionalActionList(["ThreePair", "Straight"], curRank, fullActionList)
        #print("additionalActionList", additionalActionList)
        #beginning
        bestPlay = {}
        if (len(handCards)>=15 or Strategy.roundStage != 'ending'):
            minValue = 100
            for action in handActions:
                actionValue = CountValue().ActionValue(action, action['type'], action['rank'], curRank) - Strategy.freeActionRV[action['type']] \
                        - Strategy.freeActionRV[(action['type'],action['rank'])]
                #print(action, actionValue)
                if actionValue < minValue:
                    minValue = actionValue
                    bestPlay = action
        #print(Strategy.freeActionRV[('Pair','Q')])
        else:
            maxValue = -100
            actionList = CreateActionList().CreateList(handCards)
            for i in range(0, len(config.cardTypes)):
                type = config.cardTypes[i]
                #if (type == 'StraightFlush'): continue
                for rank1 in actionList[type]:
                    for card in actionList[type][rank1]:
                        color = None
                        rank = rank1  # to distinguish StraightFlush from others
                        if (type == 'StraightFlush'):
                            rank = rank1[1]
                            color = rank1[0]
                        #print("Free play trying type, rank, card:", type, rank, card)
                        action = CreateActionList().GetAction(type, rank, card, handCards, color)
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                        thisHandValue = CountValue().ActionValue(action, type, rank, curRank)
                        thisHandValue += Strategy.freeActionRV[type]
                        if (type, rank) in Strategy.freeActionRV.keys():
                            thisHandValue += Strategy.freeActionRV[(type, rank)]
                        # print(Strategy.actionValueRevise)
                        # print(rank, card, thisHandValue, restValue)
                        if (thisHandValue < 0): thisHandValue = 0
                        if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and \
                            (bestPlay == [] or CompareRank().Smaller(type, rank, card, bestPlay, curRank)))):
                            maxValue = thisHandValue + restValue
                            bestPlay = {"action": action, "type": type, "rank": rank}
                            print(bestPlay, maxValue)

            #try additional list
            for action in additionalActionList:
                type = action[0]
                rank = action[1]
                card = rank
                if type == 'Bomb':
                    card = len(action[2])

                restCards = CreateActionList().GetRestCards(action[2], handCards)
                restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                restValue += Strategy.handRV[type]
                thisHandValue = CountValue().ActionValue(action[2], type, rank, curRank)
                thisHandValue += Strategy.freeActionRV[type]
                if (type, rank) in Strategy.freeActionRV.keys():
                    thisHandValue += Strategy.freeActionRV[(type, rank)]
                # print(Strategy.actionValueRevise)
                # print(rank, card, thisHandValue, restValue)
                if (thisHandValue < 0): thisHandValue = 0
                if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and
                                (bestPlay == [] or CompareRank().Smaller(type, rank, card, bestPlay, curRank)))):
                    maxValue = thisHandValue + restValue
                    bestPlay = {"action": action[2], "type": type, "rank": rank}
                    print('Using additional action list')
                    print(bestPlay, maxValue)

        #print("bestplay:",bestPlay, "handValue", handValue)
        return bestPlay

    def RestrictedPlay(self, handCards, formerAction, curRank, fullActionList = None):
        print("Restricted Play handCards:", handCards,"   restHandsCount:", Strategy.restHandsCount)
        actionList = CreateActionList().CreateList(handCards)

        additionalActionList = self.GetAdditionalActionList(["Bomb", "StraightFlush", "ThreePair", "Straight"], curRank,
                                                            fullActionList)
        #print("additionalActionList:", additionalActionList)

        bestPlay = []
        maxValue, restActions = CountValue().HandCardsValue(handCards, 0, curRank)
        Strategy.SetRole(maxValue, restActions, curRank)
        Strategy.makeReviseValues()
        maxValue += Strategy.restrictedActionRV["PASS"]

        #print(maxValue)
        toc = time.time()
        #print(toc - tic)

        for i in range(0, len(config.cardTypes)):
            type = config.cardTypes[i]
            #print(type, formerAction["type"])
            #if (type == 'StraightFlush'): continue
            if (type != 'Bomb' and type != 'StraightFlush' and type != formerAction["type"]): continue
            for rank1 in actionList[type]:
                for card in actionList[type][rank1]:
                    color = None
                    rank = rank1  # to distinguish StraightFlush from others
                    if (type == 'StraightFlush'):
                        rank = rank1[1]
                        color = rank1[0]
                    #print("Restricted play trying rank, card:", type, rank, card)
                    if (CompareRank().Larger(type, rank, card, formerAction, curRank)):
                        action = CreateActionList().GetAction(type, rank, card, handCards, color)
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                        #restValue += Strategy.handRV[type]
                        thisHandValue = CountValue().ActionValue(action, type, rank, curRank)
                        thisHandValue += Strategy.restrictedActionRV[type]
                        if (type, rank) in Strategy.restrictedActionRV.keys():
                            thisHandValue += Strategy.restrictedActionRV[(type, rank)]
                        #print(Strategy.actionValueRevise)
                        #print(rank, card, thisHandValue, restValue)
                        if (thisHandValue < 0): thisHandValue = 0
                        if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and \
                        (bestPlay==[] or CompareRank().Smaller(type, rank, card, bestPlay, curRank)))):
                            maxValue = thisHandValue + restValue
                            bestPlay = {"action": action, "type": type, "rank": rank}
                            print(maxValue, bestPlay)

        #try additional list
        for action in additionalActionList:
            type = action[0]
            rank = action[1]
            card = rank
            if type == 'Bomb':
                card = len(action[2])
            if (CompareRank().Larger(type, rank, card, formerAction, curRank)):
                restCards = CreateActionList().GetRestCards(action[2], handCards)
                restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                #restValue += Strategy.handRV[type]
                thisHandValue = CountValue().ActionValue(action[2], type, rank, curRank)
                thisHandValue += Strategy.restrictedActionRV[type]
                if (type, rank) in Strategy.restrictedActionRV.keys():
                    thisHandValue += Strategy.restrictedActionRV[(type, rank)]
                # print(Strategy.actionValueRevise)
                # print(rank, card, thisHandValue, restValue)
                if (thisHandValue < 0): thisHandValue = 0
                if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and
                                                (bestPlay == [] or CompareRank().Smaller(type, rank, card, bestPlay, curRank)))):
                    maxValue = thisHandValue + restValue
                    bestPlay = {"action": action[2], "type": type, "rank": rank}
                    print('Using additional action list')
                    print(bestPlay, maxValue)

        if (bestPlay==[]):
            bestPlay = {'action': 'PASS', 'type': 'PASS', 'rank': 'PASS'}
        #print("bestplay:", bestPlay, "maxvalue", maxValue)
        return bestPlay

    def Play(self, handCards, curRank):
        self.FreePlay(handCards, curRank)


#hand_cards = [[1, '3'], [3, '3'], [2, '5'], [3, '5'], [0, '6'], [2, '6'], [0, '7'], [2, '7'], [2, '7'], [0, '7'], [1, '8'], [2, '8'], [3, '9'], [1, '10'], [2, 'J'], [3, 'J'], [1, 'Q'], [2, 'Q'], [3, 'K'], [0, 'K'], [0, 'K'], [2, 'A'], [0, 'A'], [1, '2'], [0, '2'], [0, 'JOKER'], [0, 'JOKER']]
#cards = ['H2', 'C2', 'D3', 'S4', 'H4', 'C5', 'C5', 'S6', 'D6', 'H8', 'D8', 'S9', 'H9', 'ST', 'CT', 'SJ', 'CJ', 'DJ', 'HQ', 'DQ', 'SK', 'SA', 'HA', 'H7', 'D7', 'SB', 'HR']
#formerAction = {"action": ['H5', 'C5'], "type": 'Pair', 'rank': '5'}
#print(PlayCard().FreePlay(cards,'2'))
#print(PlayCard().RestrictedPlay(hand_cards, formerAction))

'''tic = time.time()

cards =  ['H3', 'C3', 'S4', 'C4', 'C5', 'S2', 'S2', 'H2', 'D2', 'D2']
Strategy.SetBeginning(0, cards)
Strategy.curRank = '2'
Strategy.restHandsCount=[10, 27, 15, 15]
Strategy.roundStage = 'ending'

#Strategy.UpdatePlay(1, ['Straight', '3', ['S3', 'C4', 'D5','D6','D7']], 1, ['Straight', '3', ['S3', 'C4', 'D5','D6','D7']])
fullActionList = [['ThreePair', '2', ['S2', 'D2', 'H3', 'H2', 'S4', 'C4']], ['ThreePair', '3', ['H3', 'C3', 'S4', 'C4', 'C5', 'H2']], ['Straight', 'A', ['H2', 'S2', 'H3', 'S4', 'C5']], ['Straight', '2', ['S2', 'H3', 'S4', 'C5', 'H2']]]
#print(PlayCard().RestrictedPlay(cards,{'action':['S3', 'C4', 'D5','D6','D7'], 'type': 'Striaight', 'rank': '3'}, 'K', fullActionList))
#print("RV:", Strategy.restrictedActionRV[('Single','R')])
#Strategy.UpdatePlay(-1, None, -1, None)
print(PlayCard().FreePlay(cards, '2', fullActionList))

toc = time.time()
print(toc-tic)'''

#cards = ['H2', 'C2', 'D3', 'S4', 'H4', 'C5', 'C5', 'S6', 'D6', 'H8', 'D8', 'S9', 'H9', 'ST', 'CT', 'SJ', 'CJ', 'DJ', 'HQ', 'DQ', 'SK', 'SA', 'HA', 'H7', 'D7', 'SB', 'HR']
#print(PlayCard().actBack(cards, '2'))

#print(not CompareRank().Larger('Pair', 'A', 'A', {'action': ['S6', 'H6', 'C6', 'C6'], 'type': 'Bomb', 'rank': '6'}, '3'))