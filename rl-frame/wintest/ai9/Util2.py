# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:


import json

Types = ['Single', 'Pair', 'Trips', 'ThreePair', 'ThreeWithTwo', 'TwoTrips', 'Straight', 'StraightFlush', 'Bomb']
Index = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T':9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13,
         'B': 14, 'R':15, 'JOKER':16}

class ACTIONENEMY:
    def __init__(self, cardRecorder = {}):
        self.cardRecorder = cardRecorder

    def bombUtil(self, actionList, Universal):
        # 归一化炸弹标准，大于4个的不拆开
        bombList = []
        # 不用万能配
        pre_index, pre_card_type, pre_rank, pre_action = -1, None, None, []
        for i in range(len(actionList)):
            card_type, rank, action = actionList[i]
            if card_type == 'Bomb':
                count = 0
                for j in action:
                    if j == Universal:
                        count += 1
                if count < 1:
                    if pre_rank is None:
                        pre_index, pre_card_type, pre_rank, pre_action = i, card_type, rank, action
                    elif pre_rank != rank:
                        bombList.append({'data':[pre_card_type, pre_rank, pre_action], 'index':pre_index})
                        pre_index, pre_card_type, pre_rank, pre_action = i, card_type, rank, action
                    elif pre_rank == rank and len(pre_action) < len(action):
                        bombList.append({'data':actionList[i], 'index':i})
                        pre_index, pre_card_type, pre_rank, pre_action = i, card_type, rank, action
        if pre_index > 0 and len(bombList) < 1:
            bombList.append({'data':[pre_card_type, pre_rank, pre_action], 'index':pre_index})
            return bombList
        # 实在找不到合适的炸弹，用万能配
        if len(bombList) < 1:
            for i in range(len(actionList)):
                card_type, rank, action = actionList[i]
                if card_type == 'Bomb':
                    bombList.append({'data': actionList[i], 'index': i})
                    return bombList
        return bombList

    def bool_actionWarning(self, message, myPos, WarningCard = 10):
        action, WarningCardLeft = False, False
        if myPos == 0 and (message['greaterPos'] == 3 or message['greaterPos'] == 1):
            handCardsLeft = message['publicInfo'][message['greaterPos']]['rest']
            if handCardsLeft <= WarningCard:
                WarningCardLeft = True
        elif myPos == 1 and (message['greaterPos'] == 0 or message['greaterPos'] == 2):
            handCardsLeft = message['publicInfo'][message['greaterPos']]['rest']
            if handCardsLeft <= WarningCard:
                WarningCardLeft = True
        elif myPos == 2 and (message['greaterPos'] == 3 or message['greaterPos'] == 1):
            handCardsLeft = message['publicInfo'][message['greaterPos']]['rest']
            if handCardsLeft <= WarningCard:
                WarningCardLeft = True
        elif myPos == 3 and (message['greaterPos'] == 0 or message['greaterPos'] == 2):
            handCardsLeft = message['publicInfo'][message['greaterPos']]['rest']
            if handCardsLeft <= WarningCard:
                WarningCardLeft = True

        # 1. 单张超过Jocke就炸
        # 2. 对子、3+2、3超过K就炸
        # 3. 炸弹、同花顺、钢板、连对、顺子小于10张就炸
        # use bomb fuck you
        if WarningCardLeft:
            fuckList1 = ['Single']
            fuckList2 = ['ThreeWithTwo', 'Trips', 'Pair']
            fuckList3 = ['TwoTrips', 'ThreePair', 'Straight', 'Bomb', 'StraightFlush']
            curRank = message['curRank']
            card_type, rank, actions = message['greaterAction']
            rank_index = Index[rank]
            if card_type in fuckList1 and (rank_index > 13 or rank == curRank):
                action = True
            elif card_type in fuckList2 and (rank_index > 11 or rank == curRank):
                action = True
            elif card_type in fuckList3:
                action = True
        return action

    def ActionEnemy(self, content, bombCardsLists, cardTypeList, myPos):
        act_index = 0
        Universal = 'H' + content['curRank']
        actionList = content["actionList"]
        ActionEnemyList = ['TwoTrips', 'ThreePair', 'Straight', 'ThreeWithTwo', 'Trips', 'Pair', 'Single']
        if len(actionList) == 1:
            return act_index
        for i in ActionEnemyList:
            for j in cardTypeList[i]:
                rank, action = j['rank'], j['action']
                count = 0
                for k in action:
                    if (k == Universal or k in bombCardsLists['Bomb']) or (i in ['ThreeWithTwo', 'Pair'] and k in ['SB','HR']):  # do not use current_rank
                        count += 1
                if count > 0:
                    continue
                else:
                    return j['index']
        # bomb fuck you
        if self.bool_actionWarning(content, myPos, WarningCard=10):
            bombList = self.bombUtil(actionList, Universal)
            # 先使用炸弹，不用万能配
            for i in bombList:
                index = i['index']
                card_type, rank, action = i['data']
                count = 0
                for k in action:
                    if k == Universal:  # do not use current_rank
                        count += 1
                if count > 0:
                    continue
                else:
                    return index
            # 使用炸弹，用万能配
            for i in bombList:
                index = i['index']
                return index
            # 先使用同花顺，不用万能配
            for i in range(len(actionList)):
                card_type, rank, action = actionList[i]
                if card_type == 'StraightFlush':
                        count = 0
                        for k in action:
                            if k == Universal:  # do not use current_rank
                                count += 1
                        if count > 0:
                            continue
                        else:
                            return i
            # 使用同花顺，用万能配
            for i in range(len(actionList)):
                return i
        return act_index

class ACTIONTEAM:
    def __init__(self, cardRecorder = {}):
        self.cardRecorder = cardRecorder

    def bool_action_team(self, message, myPos):
        action = False
        if myPos == 0 and message['greaterPos'] == 2:
            action = True
        elif myPos == 1 and message['greaterPos'] == 3:
            action = True
        elif myPos == 2 and message['greaterPos'] == 0:
            action = True
        elif myPos == 3 and message['greaterPos'] == 1:
            action = True
        return action

    # 压队友的牌
    def ActionTeam(self, content, bombCardsLists, cardTypeList, fuckRank = 10):
        act_index = 0
        actionList = content["actionList"]
        Universal = 'H' + content['curRank']
        count = 0
        ActionTeamList = ['ThreeWithTwo', 'Trips', 'Pair', 'Single']
        for i in ActionTeamList:
            for j in cardTypeList[i]:
                rank, action = j['rank'], j['action']
                _, team_rank, _ = content['greaterAction']
                rank_index = Index[team_rank]
                if max(rank_index, Index[rank]-2) < fuckRank or (i=='Single' and Index[rank]<14): # 队友的牌面小于Q才压
                    for k in action:
                        if list(k)[1] == content['curRank'] or k in bombCardsLists['Bomb']:  # do not use current_rank
                            count += 1
                    if count > 0:
                        count = 0
                        continue
                    else:
                        return j['index']
        return act_index

class ACTIONFIRST:
    def __init__(self, cardRecorder = {}):
        self.cardRecorder = cardRecorder

    def find_max_rank(self, action_list, card_type):
        max_rank = 0
        for i in action_list:
            cur_card_type, cur_rank, cur_action = i
            if card_type == cur_card_type and Index[cur_rank] > max_rank:
                max_rank = Index[cur_rank]
        return max_rank

    def get_best_action(self, message, bombCardsLists, cardTypeList, cardIndex = 10, boolWarningCard = False):
        act_index = -1
        Universal = 'H' + message['curRank']
        action_list = message["actionList"]
        if boolWarningCard:
            ScoreListTotle = {'TwoTrips': 0, 'ThreePair': 1, 'Straight': 2, 'ThreeWithTwo': 3, 'Pair': 4, 'Single': 5,
                              'Trips': 6, 'Bomb': 7, 'StraightFlush': 8}
            for i in ScoreListTotle:
                for j in cardTypeList[i]:
                    cur_rank, cur_action = j['rank'], j['action']
                    count = 0
                    for k in cur_action:
                        if k == Universal or k in bombCardsLists['Bomb']:  # do not use current_rank
                            count += 1
                    if count > 0:
                        continue
                    else:
                        return j['index']
        else:
            ScoreList_1 = {'TwoTrips': 0, 'ThreePair': 1, 'Straight': 2}
            ScoreList_2 = {'ThreeWithTwo': 0, 'Pair': 1, 'Trips': 2}
            ScoreList_3 = {'Single': 0}

            for i in ScoreList_1:
                for j in cardTypeList[i]:
                    cur_rank, cur_action = j['rank'], j['action']
                    if (cur_rank == '' or Index[cur_rank] < cardIndex) and cur_rank != message['curRank']:  # 大于J的不出
                        count = 0
                        for k in cur_action:
                            if Universal == k or (k in bombCardsLists['Bomb'] or k in bombCardsLists['StraightFlush']):  # do not use current_rank
                                count += 1
                        if count > 0:
                            continue
                        else:
                            return j['index']
            for i in ScoreList_2:
                for j in cardTypeList[i]:
                    cur_rank, cur_action = j['rank'], j['action']
                    max_rank = self.find_max_rank(action_list, i)
                    if Index[cur_rank] > cardIndex-1 or cur_rank == message['curRank']:
                        continue
                    count = 0
                    for k in cur_action:
                        if list(k)[1] == message['curRank'] or k in bombCardsLists['Bomb']:  # do not use current_rank
                            count += 1
                    if count > 0:
                        continue
                    else:
                        return j['index']
            for i in ScoreList_3:
                for j in cardTypeList[i]:
                    cur_rank, cur_action = j['rank'], j['action']
                    if cur_rank == message['curRank'] or\
                            (cur_action[0] in bombCardsLists['Bomb'] or cur_action[0] in bombCardsLists['StraightFlush']):
                        continue
                    max_rank = self.find_max_rank(action_list, i)
                    if Index[cur_rank] > cardIndex+1:
                        continue
                    else:
                        return j['index']
        return act_index

    def ActionFirst(self, message, bombCardsLists, cardTypeList, WarningCard = 10):
        act_index = -1
        action_list = message["actionList"]
        # 贡牌tribute, back
        if 'back' == message['stage']:
            # 先找单张
            for i in cardTypeList['Single']:
                return i['index']
            if act_index < 0:
                return 0
        elif 'tribute' == message['stage']:
            for i in range(len(action_list)):
                return i
        else: # 'anti-tribute', others
            if len(message['handCards']) > WarningCard:
                # 先找最优的出牌策略
                act_index = self.get_best_action(message, bombCardsLists, cardTypeList, cardIndex=10, boolWarningCard = False)
                if act_index < 0:
                    ScoreList = {'TwoTrips': 0, 'ThreePair': 1, 'ThreeWithTwo': 2, 'Straight': 3, 'Pair': 4,
                                     'Single': 5, 'Trips': 6}
                    for i in ScoreList:
                        for j in cardTypeList[i]:
                            return j['index']
                else:
                    return act_index
            else:
                act_index = self.get_best_action(message, bombCardsLists, cardTypeList, cardIndex=10, boolWarningCard=True)
                if act_index < 0:
                    ScoreListTotle = {'TwoTrips': 0, 'ThreePair': 1, 'Straight': 2, 'ThreeWithTwo': 3, 'Pair': 4, 'Single': 5,
                                 'Trips': 6, 'Bomb': 7, 'StraightFlush': 8}
                    for i in ScoreListTotle:
                        for j in cardTypeList[i]:
                            return j['index']
                else:
                    return act_index