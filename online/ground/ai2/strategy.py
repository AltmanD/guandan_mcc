import config
import CountValue


class Strategy(object):
    def Clear(self):
        self.roundStage = ''
        self.role = ''
        self.freeActionRV = {}  # RV = revised value
        self.restrictedActionRV = {}
        self.handRV = {}
        self.restCardsCount = {}
        self.restHandsCount = []
        self.PlayersTypeMsg = None
        self.curPos = -1
        self.greaterPos = -1
        self.myPos = -1
        self.greaterAction = None
        self.curAction = None
        self.curRank = None
        self.recordPlayerActions = [{}, {}, {}, {}]

    def __init__(self):
        self.Clear()

    def foo(self):
        pass

    def SetBeginning(self, myPos, handCard):
        self.Clear()
        self.roundStage = 'beginning'
        self.myPos = myPos
        self.restHandsCount = [27, 27, 27, 27]
        self.recordPlayerActions = [{}, {}, {}, {}]
        for rank in config.cardRanks:
            if rank == 'B' or rank == 'R':
                self.restCardsCount[rank] = 2
            else:
                self.restCardsCount[rank] = 4
        for card in handCard:
            self.restCardsCount[card[1]] -= 1
        for type in config.cardTypes:
            for rank in config.cardRanks:
                self.restrictedActionRV[(type, rank)] = 0
                self.freeActionRV[(type, rank)] = 0

    def SetRole(self, handValue, handActions, curRank):
        countBombs = 0
        countBigs = 0
        countSmalls = 0
        for action in handActions:
            actionValue = CountValue.CountValue().ActionValue(action, action['type'], action['rank'], curRank)
            if action['type'] == 'Bomb' or action['type'] == 'StraightFlush':
                countBombs += 1
            elif actionValue < 0:
                countSmalls += 1
            else:
                countBigs += 1
        # print(handValue, handActions, curRank)
        # print('bombs:',countBombs,'bigs',countBigs,'smalls:',countSmalls)
        self.role = ""
        if (countSmalls <= 3 and countBombs >= 3):
            self.role += "active attack"
        elif (countSmalls <= 3 and countBigs >= 3):
            self.role += "active defense"
        elif (countSmalls <= 3 and countBombs < 3):
            self.role += "defense"
        elif (countBigs > 3 and countBombs >= 3):
            self.role += "pair attack"
        elif (countSmalls > 3 and countBigs >= 3):
            self.role += "pair defense"
        elif (countSmalls > 3):
            self.role = "pair defense"

    def UpdateCurRank(self, curRank):
        self.curRank = curRank

    def UpdatePlay(self, curPos, curAction, greaterPos, greaterAction):  # '3', ['Pair','3','['S3','H3']]
        # print("UpdatePlay:", curPos, curAction, greaterPos, greaterAction)
        if (curAction[0] != 'PASS'):
            self.restHandsCount[curPos] -= len(curAction[2])
        if (self.restHandsCount[curPos] <= 10):
            self.roundStage = 'ending'
        self.curAction = curAction
        self.curPos = curPos
        self.greaterPos = greaterPos
        self.greaterAction = greaterAction

        if (curAction[0] == 'PASS'):  # update recordPlayerActions
            type = greaterAction[0]
            rank = 'PASS'
        elif (curAction[0] == 'Bomb' and greaterAction[0] != 'Bomb'):
            type = greaterAction[0]
            rank = 'Bomb'
        else:
            type = curAction[0]
            rank = curAction[1]

        if type not in self.recordPlayerActions[curPos].keys():
            self.recordPlayerActions[curPos][type] = [rank]
        else:
            self.recordPlayerActions[curPos][type].append(rank)
        if (curPos != self.myPos and curAction[0] != 'PASS'):
            for card in curAction[2]:
                self.restCardsCount[card[1]] -= 1

    def UpdateRVByRoleAtBeginning(self):
        if (self.roundStage != 'beginning'):
            return
        if ('defense' in self.role):
            self.restrictedActionRV['Bomb'] = max(-0.5, self.restrictedActionRV['Bomb'] - 0.5)
            self.restrictedActionRV['StraightFlush'] = max(-0.5, self.restrictedActionRV['StraightFlush'] - 0.5)
            self.handRV["Bomb"] = 0
        if ('active' in self.role):
            self.restrictedActionRV['Bomb'] = 0
            self.handRV["Bomb"] = max(-0.5, self.handRV['Bomb'] - 0.5)
            # print('here')

    def UpdateRVATBeginning(self):
        if (self.roundStage != 'beginning'):
            return
        if (self.restHandsCount[self.myPos] == 27):
            for rank in config.cardRanks:
                if rank in ['J', 'Q', 'K']:
                    self.freeActionRV[('Pair', rank)] = max(-0.5, self.freeActionRV[('Pair', rank)] - 0.5)
                    self.freeActionRV[('Trips', rank)] = max(-0.5, self.freeActionRV[('Trips', rank)] - 0.5)
                    self.freeActionRV[('ThreeWithTwo', rank)] = max(-0.5,
                                                                    self.freeActionRV[('ThreeWithTwo', rank)] - 0.5)
                    # if rank in ['3','4','5']:
                    #    self.freeActionRV[('Single', rank)] = max(-0.5, self.freeActionRV[('Single', rank)] - 0.5)

    def UpdateRVATEnding(self):
        if (self.roundStage != 'ending'):
            return
        self.restrictedActionRV['Bomb'] = max(0, self.restrictedActionRV['Bomb'])
        self.restrictedActionRV['StraightFlush'] = max(0, self.restrictedActionRV['StraightFlush'])
        self.freeActionRV["Bomb"] = max(-0.5, self.freeActionRV['Bomb'] - 0.5)
        self.freeActionRV["StraightFlush"] = max(-0.5, self.freeActionRV['StraightFlush'] - 0.5)
        self.handRV["Bomb"] = 0
        self.freeActionRV["Straight"] = min(1, self.freeActionRV['Straight'] + 0.5)
        self.restrictedActionRV["Straight"] = min(1, self.restrictedActionRV['Straight'] + 0.5)
        self.handRV["Straight"] = max(-1, self.handRV['Straight'] - 0.5)
        self.freeActionRV["TwoTrips"] = min(1, self.freeActionRV['TwoTrips'] + 0.5)
        self.restrictedActionRV["TwoTrips"] = min(1, self.restrictedActionRV['TwoTrips'] + 0.5)
        self.handRV["TwoTrips"] = max(-1, self.handRV['TwoTrips'] - 0.5)
        self.freeActionRV["ThreePair"] = min(1, self.freeActionRV['ThreePair'] + 0.5)
        self.restrictedActionRV["ThreePair"] = min(1, self.restrictedActionRV['ThreePair'] + 0.5)
        self.handRV["ThreePair"] = max(-1, self.handRV['ThreePair'] - 0.5)

    '''def UpdateRVByRestHandsCount(self):
        if (self.roundStage != 'ending'):
            return
        C_part = self.restHandsCount[(self.myPos+2)%4]
        C_oppo = [self.restHandsCount[(self.myPos+1)%4], self.restHandsCount[(self.myPos+3)%4]]
        if (C_part == 1):
            self.freeActionRV['Single'] += 1
        elif (C_part == 2):
            self.freeActionRV['Pair'] += 1
        if (C_part == 5):
            self.freeActionRV['Pair'] -= 1
            self.freeActionRV['ThreeWithTwo'] += 0.5
        if (1 in C_oppo):
            self.freeActionRV['Single'] -= 1
        elif (2 in C_oppo):
            self.freeActionRV['Pair'] -= 1
        if (5 in C_oppo):
            self.freeActionRV['Pair'] += 1
            self.freeActionRV['ThreeWithTwo'] -= 1'''

    def UpdateRVByRestHandsCount(self):
        if (self.roundStage != 'ending'):
            return
        part = (self.myPos + 2) % 4
        C_part = self.restHandsCount[part]
        oppo1 = (self.myPos + 1) % 4
        C_oppo1 = self.restHandsCount[oppo1]
        oppo2 = (self.myPos + 3) % 4
        C_oppo2 = self.restHandsCount[oppo2]
        C_oppo = [C_oppo1, C_oppo2]
        if (C_part == 1):
            self.freeActionRV['Single'] += 1
        elif (C_part == 2):
            self.freeActionRV['Pair'] += 1
        if (C_part == 5):
            self.freeActionRV['Pair'] -= 1
            self.freeActionRV['ThreeWithTwo'] += 0.5
        if (1 in C_oppo):
            self.freeActionRV['Single'] -= 1
            self.restrictedActionRV['Single'] += 0.5
            # print('here')
        elif (2 in C_oppo):
            self.freeActionRV['Pair'] -= 1
        if (5 in C_oppo):
            self.freeActionRV['Pair'] += 1
            self.freeActionRV['ThreeWithTwo'] -= 0.5
        # print(oppo1, oppo2, self.greaterPos)
        if (C_oppo1 < 5 and C_oppo1 != 4 and oppo1 == self.greaterPos):
            self.restrictedActionRV['PASS'] -= 1
        if (C_oppo2 < 5 and C_oppo2 != 4 and oppo2 == self.greaterPos):
            self.restrictedActionRV['PASS'] -= 0.5
        if (C_part < 5 and part == self.greaterPos):
            self.restrictedActionRV['PASS'] += 0.5

    def UpdateRVWhenPartnerControls(self):
        if (self.greaterPos == (self.myPos + 2) % 4):
            self.restrictedActionRV['Bomb'] = -1.5
            self.restrictedActionRV["StraightFlush"] = -1.5
            self.restrictedActionRV["Single"] = max(-1, self.restrictedActionRV['Single'] - 0.5)
            self.restrictedActionRV["Pair"] = max(-1, self.restrictedActionRV['Pair'] - 0.5)
            self.restrictedActionRV["Trips"] = max(-1, self.restrictedActionRV['Trips'] - 0.5)
            self.restrictedActionRV["Straight"] = max(-1, self.restrictedActionRV['Straight'] - 0.5)
            self.restrictedActionRV["ThreeWithTwo"] = max(-1, self.restrictedActionRV['ThreeWithTwo'] - 0.5)

    def UpdateRVwhenOppoPlaysSmall(self):
        if (self.greaterPos != (self.myPos + 1) % 4 and self.greaterPos != (self.myPos + 3) % 4):
            self.restrictedActionRV["PASS"] = 0
            return
        elif (self.greaterPos == (self.myPos + 1) % 4):
            oppoHandValue = CountValue.CountValue().ActionValue(self.curAction[2], self.curAction[0], self.curAction[1],
                                                                self.curRank)
            part = (self.myPos + 2) % 4
            if self.curAction[0] in self.recordPlayerActions[part].keys():
                if self.recordPlayerActions[part][self.curAction[0]][-1] in ['PASS', 'Bomb']:
                    self.restrictedActionRV["PASS"] = max(-1, min(0, oppoHandValue))
                    return
        self.restrictedActionRV["PASS"] = 0
        return

    def UpdateRVByPlayerActions(self):
        oppo1 = (self.myPos + 1) % 4
        # part = (self.myPos+2)%4
        oppo2 = (self.myPos + 3) % 4
        for type in config.cardTypes:
            count = 0
            if type in self.recordPlayerActions[oppo1].keys():
                playList = self.recordPlayerActions[oppo1][type]
                if (len(playList) >= 2 and playList[-1] in ['PASS', 'Bomb'] and playList[-2] in ['PASS', 'Bomb']):
                    count += 1
            if type in self.recordPlayerActions[oppo2].keys():
                playList = self.recordPlayerActions[oppo2][type]
                if (len(playList) >= 2 and playList[-1] in ['PASS', 'Bomb'] and playList[-2] in ['PASS', 'Bomb']):
                    count += 1
            if count == 2:
                self.freeActionRV[type] += min(1, self.freeActionRV[type] + 1)

    def UpdateRVwhenRushing(self):
        C_myself = self.restHandsCount[self.myPos]
        if (C_myself > 5):
            return
        if C_myself == 2:
            self.restrictedActionRV['Single'] = max(0.5, self.restrictedActionRV['Single'] + 0.5)
            self.restrictedActionRV['PASS'] = min(-1, self.restrictedActionRV['PASS'] - 0.5)
        if C_myself == 3 or C_myself == 4:
            self.restrictedActionRV['Single'] = max(0.5, self.restrictedActionRV['Single'] + 0.5)
            self.restrictedActionRV['Pair'] = max(0.5, self.restrictedActionRV['Pair'] + 0.5)
            self.restrictedActionRV['PASS'] = min(-1, self.restrictedActionRV['PASS'] - 0.5)

    def UpdateRVbyRestCardsCount(self):
        C_R = self.restCardsCount['R']
        C_B = self.restCardsCount['B']
        C_rank = self.restCardsCount[self.curRank]
        if (C_R == 0 and C_B != 0):
            self.restrictedActionRV[('Single', 'B')] += 0.5
            self.restrictedActionRV[('Pair', 'B')] += 0.5
        elif (C_R == 0 and C_B == 0):
            self.restrictedActionRV[('Single', self.curRank)] += 0.5
            self.restrictedActionRV[('Pair', self.curRank)] += 0.5
            if (C_rank == 0):
                self.restrictedActionRV[('Trips', 'A')] += 0.5
                self.restrictedActionRV[('ThreeWithTwo', 'A')] += 0.5

    def makeReviseValues(self):
        for type in config.cardTypes:
            self.restrictedActionRV[type] = 0
            self.freeActionRV[type] = 0
            self.handRV[type] = 0
        self.UpdateRVByRoleAtBeginning()
        self.UpdateRVATBeginning()
        self.UpdateRVATEnding()
        self.UpdateRVByRestHandsCount()
        self.UpdateRVWhenPartnerControls()
        self.UpdateRVwhenOppoPlaysSmall()
        self.UpdateRVByPlayerActions()
        self.UpdateRVwhenRushing()
        self.UpdateRVbyRestCardsCount()


Strategy = Strategy()
