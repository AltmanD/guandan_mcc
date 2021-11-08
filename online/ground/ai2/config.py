cardRanks=['2','3','4','5','6','7','8','9','T','J','Q','K','A','B','R']
cardColors=['S','H','C','D']
#cardTypes=['StraightFlush', 'Bomb', 'ThreePair', 'TwoTrips', 'ThreeWithTwo', 'Straight', 'Trips', 'Pair', 'Single']
cardTypes=['StraightFlush', 'Bomb', 'ThreePair', 'TwoTrips', 'Straight', 'ThreeWithTwo', 'Trips', 'Pair', 'Single']

class CompareRank():
    def Larger(self, type, rank, card, formerAction, curRank): #('Straight','5','9',['S4','S5','H6','H7,'D8']) -> True
        if (rank == 'JOKER'):   # all 4 Jokers
            return True
        elif (formerAction['rank'] == 'JOKER'):
            return False
        if ((type == 'StraightFlush' or type == 'Bomb') and formerAction['type']!='Bomb' and formerAction['type']!='StraightFlush'):
            return True
        if (type != 'Bomb' and type != 'StraightFlush' and (formerAction['type'] == 'Bomb' or formerAction['type'] == 'StraightFlush')):
            return False

        r1 = cardRanks.index(rank)
        r2 = cardRanks.index(formerAction['rank'])

        #print(type, r1, r2)
        if (type=='Bomb'):
            if (formerAction['type']=='Bomb'):
                if (card>len(formerAction['action'])):
                    return True
                elif (card<len(formerAction['action'])):
                    return False
                else:
                    return r1 > r2
            elif (formerAction['type']=='StraightFlush'):
                if card>5:
                    return True
                else:
                    return False
            else:
                return True
        elif (type=='StraightFlush'):
            if (formerAction['type'] == 'Bomb'):
                if (len(formerAction['action']) <= 5):
                    return True
                else:
                    return False
            elif (formerAction['type'] == 'StraightFlush'):
                if (r1 == cardRanks.index('A')): r1 = -1
                if (r2 == cardRanks.index('A')): r2 = -1
                return r1 > r2
            else:
                return True
        elif (type=='Trips' or type=='Pair' or type=='Single' or type=='ThreeWithTwo'):
            if rank == curRank:
                r1 = cardRanks.index('A') + 0.5
            if formerAction['rank'] == curRank:
                r2 = cardRanks.index('A') + 0.5
            return r1 > r2
        elif (type=='ThreePair' or type=='TripsPair' or type=='Straight'):
            if (r1 == cardRanks.index('A')): r1 = -1
            if (r2 == cardRanks.index('A')): r2 = -1
            return r1 > r2

    def Smaller(self, type, rank, card, formerAction, curRank):  # ('Straight','5','9',['S4','S5','H6','H7,'D8']) -> False
        if (type == formerAction['type'] and rank == formerAction['rank']):
            if (type == 'ThreeWithTwo'):
                formerCard = ''
                for action in formerAction['action']:
                    if action[1]!=formerAction['rank']:
                        formerCard = action[1]
                r1 = cardRanks.index(card)
                r2 = cardRanks.index(formerCard)
                if card == curRank:
                    r1 = cardRanks.index('A') + 0.5
                if formerCard == curRank:
                    r2 = cardRanks.index('A') + 0.5
                return r1 < r2
            else:
                return False
        else:
            return not self.Larger(type, rank, card, formerAction, curRank)

#print(CompareRank().Larger('Bomb','T',4,{'type':'Bomb','rank':'A','action':['SA', 'HA', 'HA', 'DA']}, 'T'))

#print(not CompareRank().Larger('Pair', 'A', 'A', {'action': ['S6', 'H6', 'C6', 'C6'], 'type': 'Bomb', 'rank': '6'}, '3'))

#print(CompareRank().Smaller('ThreeWithTwo','J','T',{'type':'ThreeWithTwo','rank':'J','action':['S4', 'H4', 'SJ', 'SJ', 'CJ']}, '2'))