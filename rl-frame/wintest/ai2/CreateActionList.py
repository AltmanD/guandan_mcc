import json
import random
import config

class CreateActionList():

    def MakeContinous(self,handCards, length, number):
        listCards = []
        listThreePair = {}
        for rank in config.cardRanks:
            l = [item[1] for item in handCards if rank == item[1]]
            listCards.append(l)
        for i in range(0,len(listCards)-length-1):
            f=True
            for j in range(0,length):
                if (len(listCards[i+j])<number):
                    f=False
                    break
            if (f):
                #l=[listCards[i+j][0] for j in range(0, length)]
                l=[listCards[i+length-1][0]]
                listThreePair[listCards[i][0]]=l
        f = True
        for i in range(0, length-1):
            if (len(listCards[i]) < number):
                f=False
                break
        if (f and len(listCards[-3])>=number):
            #l = ['A']+[listCards[j][0] for j in range(0, length-1)]
            l=[config.cardRanks[length-2]]
            listThreePair['A'] = l
        return listThreePair

    def CreateSingle(self,handCards):  #['S2','S3']->{'2':[2],'3':[3]}
        listSingle={}
        for type in config.cardRanks:
            l=[item[1] for item in handCards if type==item[1]]
            if l: listSingle[type]=list(set(l))
        return listSingle

    def CreatePair(self,handCards):
        listPair = {}
        for type in config.cardRanks:
            l=[item[1] for item in handCards if type==item[1]]
            if (len(l)>=2): listPair[type]=list(set(l))
        return listPair

    def CreateTrips(self,handCards):
        listTrips = {}
        for type in config.cardRanks:
            l=[item[1] for item in handCards if type==item[1]]
            if (len(l)>=3): listTrips[type]=list(set(l))
        return listTrips

    def CreateThreePair(self,handCards):
        listThreePair = self.MakeContinous(handCards, 3, 2)
        return listThreePair

    def CreateTwoTrips(self,handCards):
        CreateTwoTrips = self.MakeContinous(handCards, 2, 3)
        return CreateTwoTrips

    def CreateStraight(self,handCards):
        CreateStraight = self.MakeContinous(handCards, 5, 1)
        return CreateStraight

    def CreateBomb(self,handCards):
        listBomb = {}
        for type in config.cardRanks:
            l=[item[1] for item in handCards if type==item[1]]
            if (len(l)>=4):
                listBomb[type]=[i for i in range(4,len(l)+1)]
                listBomb[type].reverse()
        return listBomb

    def CreateThreeWithTwo(self, handCards):
        listThreeWithTwo = {}
        listCards = []
        for type in config.cardRanks:
            l = [item[1] for item in handCards if type == item[1]]
            listCards.append(l)
        for i in range(0,len(config.cardRanks)):
            if len(listCards[i])>=3:
                l=[item[0] for item in listCards if (len(item)>=2 and item[0]!=listCards[i][0]) ]
                listThreeWithTwo[listCards[i][0]]=l
        return listThreeWithTwo

    def CreateStraightFlush(self, handCards):
        listStraightFlush = {}
        for i in range(0, config.cardRanks.index('J')):
            for j in config.cardColors:
                if j+config.cardRanks[i] in handCards:
                    f=True
                    for k in range(0,5):
                        if not (j+config.cardRanks[i+k] in handCards):
                            f=False
                            break
                    if (f):
                        #l=[config.cardRanks[i+k] for k in range(0,5)]
                        l=[config.cardRanks[i+4]]
                        listStraightFlush[j,config.cardRanks[i]]=l
        for j in config.cardColors:
            if j+'A' in handCards:
                if (j+'2' in handCards and j+'3' in handCards and j+'4' in handCards and j+'5' in handCards):
                    #l = ['A']+[config.cardRanks[k] for k in range(0, 4)]
                    l=['5']
                    listStraightFlush[j, 'A'] = l
        return listStraightFlush

    def TestList(self,handCards):
        actionList={}
        actionList['StraightFlush'] = self.CreateStraightFlush(handCards)
        return actionList

    def CreateList(self,handCards):
        actionList={}
        actionList['Single']=self.CreateSingle(handCards)
        actionList['Pair'] = self.CreatePair(handCards)
        actionList['Trips'] = self.CreateTrips(handCards)
        actionList['ThreeWithTwo'] = self.CreateThreeWithTwo(handCards)
        actionList['ThreePair'] = self.CreateThreePair(handCards)
        actionList['TwoTrips'] = self.CreateTwoTrips(handCards)
        actionList['Straight'] = self.CreateStraight(handCards)
        actionList['StraightFlush'] = self.CreateStraightFlush(handCards)
        actionList['Bomb'] = self.CreateBomb(handCards)
        return actionList

    def MakeCount(self, type, rank, card):
        count={}
        if type == 'Single':
            count[rank] = 1
        elif type == 'Pair':
            count[rank] = 2
        elif type == 'Trips':
            count[rank] = 3
        elif type == 'Bomb':
            count[rank] = card
        elif type == 'ThreeWithTwo':
            count[rank] = 3
            count[card] = 2
        elif type == 'ThreePair':
            if rank=='A':
                count['A']=count['2']=count['3']=2
            else:
                pos=config.cardRanks.index(rank)
                for i in range(0,3):
                    count[config.cardRanks[pos+i]]=2
        elif type =='TwoTrips':
            if rank=='A':
                count['A']=count['2']=3
            else:
                pos=config.cardRanks.index(rank)
                for i in range(0,2):
                    count[config.cardRanks[pos+i]]=3
        elif type =='Straight':
            if rank=='A':
                count['A']=count['2']=count['3']=count['4']=count['5']=1
            else:
                pos=config.cardRanks.index(rank)
                for i in range(0,5):
                    count[config.cardRanks[pos+i]]=1
        return count

    def GetAction(self, type, rank, card, handCards, color = None):  #('Pair', '2', '2',handCards) -> ['SA', 'SA']
        action = []
        if (type == 'StraightFlush'):
            if rank=='A':
                action.append(color + 'A')
                pos = config.cardRanks.index('2')
                for i in range(0,4):
                    action.append(color + config.cardRanks[pos+i])
            else:
                pos = config.cardRanks.index(rank)
                for i in range(0,5):
                    action.append(color + config.cardRanks[pos+i])
            return action

        count = self.MakeCount(type, rank, card)
        for item in handCards:
            if (item[1] in count and count[item[1]]>0):
                action.append(item)
                count[item[1]]-=1
        return action

    def GetRestCards(self, action, handCards):
        restCards = [item for item in handCards]
        for card in action:
            if card in restCards:
                restCards.remove(card)
        #print(card, restCards)
        return restCards



#cards=['S2', 'H3', 'S3', 'D3', 'S4', 'C4', 'S5', 'S6', 'S7', 'C7', 'D7', 'SA', 'D9', 'ST', 'HT', 'CT', 'HJ', 'HJ', 'CQ', 'DQ', 'SK', 'CK', 'CA', 'CA', 'H8', 'H8', 'C8']#cards = ['SA', 'SA', 'HA', 'CA', 'S2', 'C2', 'C2', 'S3', 'S3', 'H3', 'S4', 'S4', 'S5', 'S5', 'S6', 'SQ', 'SQ', 'SK', 'SK']
#cards=['HA', 'CK', 'SQ', 'SJ','SB','ST','S9']
#print(CreateActionList().GetAction('Pair', '2', '2', cards))
#print(CreateActionList().CreateStraight(cards))
#print(CreateActionList().GetAction('StraightFlush', 'A', '6',cards, 'S'))
