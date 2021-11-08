# -*- coding: utf-8 -*-
# @Time       : 12020/10/1 21:32
# @Author     : Duofeng Wu
# @File       : action.py
# @Description: 动作类

from random import randint
import copy
from utils import *
# from utils import combine_handcards,rest_cards,is_inStraight,choose_bomb,cal_bomb_num,getindex,rankone,ranktwo,rankthree,rankfour
# from utils import one_hand
from random import random

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

    def __init__(self,name):
        self.action = []
        self.act_range = -1

    def Single(self,actionList,curAction,rank_card,handcards,numofplayers,rest_cards,card_val,myPos,greaterPos,pass_num,my_pass_num):
        numofnext = numofplayers[(myPos+1)%4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]
        numofmy = numofplayers[myPos]
        numofpre = numofplayers[(myPos - 1) % 4]


        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"])!=0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"])!=0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        tag = 0
        single_actionList = []
        bomb_actionList = []
        for action in actionList[1:]:
            tag += 1
            if action[0] == 'Single':
                single_actionList.append((tag,action))
            else:
                bomb_actionList.append((tag,action))

        curVal = card_val[curAction[1]]

        max_val = card_val[rest_cards[-1][0][1]]

        if numofnext == 0:
            numofnext = numofplayers[(myPos-1)%4]

        if numofnext <= 4 or (numofpre <= 3 and numofpre>=1):
            if (myPos+2)%4 == greaterPos and curVal >= max_val:
                return 0
            if (myPos+2)%4 == greaterPos and curVal>=15 and numofnext!=1:
                return 0

            for action in single_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]]>= max_val and action[2][0] in single_member and rank_card not in action[2]:
                    return Index

            for action in single_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val and action[2][0] not in bomb_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index

            index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
            if index!=-1:
                return index

            for action in single_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val-2 and action[2][0] not in bomb_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index

            for action in single_actionList:
                Index = action[0]
                action = action[1]
                if rank_card in action[2] and (len(sorted_cards["Pair"])<3 or numofnext==1):
                    return Index

        def normal(single_actionList,single_member,rank_card):
            for action in single_actionList:
                Index = action[0]
                action = action[1]
                if (action[2][0] in single_member or card_val[action[1]] >= 15) and rank_card not in action[2]:
                    return Index
            return -1

        def special(single_actionList,bomb_member,straight_member,rank_card):
            for action in single_actionList[::-1]:
                Index = action[0]
                action = action[1]
                if action[2][0] not in bomb_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index
            return -1

        if (myPos+2)%4 == greaterPos:
            if curVal >= 14 or curVal >= max_val-2:
                return 0
            elif numoffri <= 4 :
                index = normal(single_actionList, single_member,rank_card)
                if index == -1:
                    return 0
                if curVal <= 10:
                    return index
                else:
                    print(index)
                    if card_val[actionList[index][1]] == curVal+1:
                        return index
            else:
                index = normal(single_actionList,single_member,rank_card)
                if index!=-1:
                    return index
                else:
                    return 0
        else:
            index = normal(single_actionList,single_member, rank_card)
            if index!=-1:
                return index
            else:
                if pass_num >= 5 or my_pass_num >= 3:
                    index = special(single_actionList, bomb_member, straight_member, rank_card)
                    if index != -1:
                        return index
                cur_bomb_num = cal_bomb_num(sorted_cards, handcards, rank_card)
                if curVal >= max_val and numofgreaterPos >= 15 and cur_bomb_num > 1:
                    p = random()
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if p > 0.5:
                        if index != -1:
                            return index
                elif ((curVal >= 15 or curVal>=max_val-2)  and numofgreaterPos <= 15) or pass_num >= 7 or my_pass_num >= 5:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index != -1:
                        return index
                    else:
                        return 0

        return 0

    def Pair(self,actionList,curAction,rank_card,handcards,numofplayers,rest_cards,card_val,myPos,greaterPos,pass_num,my_pass_num):

        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]
        numofpre = numofplayers[(myPos-1)%4]
        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        pair_actionList = []
        bomb_actionList = []
        tag = 0
        for action in actionList[1:]:
            tag += 1
            if action[0] == 'Pair':
                pair_actionList.append((tag,action))
            else:
                bomb_actionList.append((tag,action))

        curVal = card_val[curAction[1]]
        rest_cards = rest_cards[::-1]
        max_val = 0
        for cards in rest_cards:
            if len(cards) >= 2:
                max_val = card_val[cards[0][1]]
                break
        if numofnext == 0:
            numofnext = numofplayers[(myPos-1)%4]

        if numofnext <= 4 or (numofpre <= 4 and numofpre>=1):

            if (myPos+2)%4 == greaterPos and curVal>=max_val:
                return 0
            if (myPos+2)%4 == greaterPos and curVal>=12 and numofnext!=2:
                return 0

            for action in pair_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val and action[2][0] in pair_member and rank_card not in action[2]:
                    return Index

            for action in pair_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val and action[2][0] not in bomb_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index

            index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
            if index != -1:
                return index

            for action in pair_actionList[::-1]:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val-2 and action[2][0] not in bomb_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index

            max_match = -1
            max_match_index = -1
            for action in pair_actionList:
                index = action[0]
                action = action[1]
                if rank_card in action[2] and card_val[action[1]] > max_match and action[2][0] not in bomb_member:
                    if is_inStraight(action, straight_member):
                        continue
                    max_match = card_val[action[1]]
                    max_match_index = index
            if max_match_index != -1 and max_match>=max_val-2:
                return max_match_index

        def normal(pair_actionList,pair_member,rank_card):
            for action in pair_actionList:
                Index = action[0]
                action = action[1]
                if (action[2][0] in pair_member or action[1]==rank_card[1]) and rank_card not in action[2] :
                    return Index

            return -1

        def special(pair_actionList,bomb_member,straight_member,rank_card):
            for action in pair_actionList[::-1]:
                Index = action[0]
                action = action[1]

                if action[2][0] not in bomb_member  and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index
            return -1

        if (myPos+2)%4 == greaterPos:
            if curVal >= 13 or curVal >= max_val-2:
                return 0
            elif numoffri <= 4:
                index = normal(pair_actionList,pair_member,rank_card)
                if index == -1:
                    return 0
                if curVal <= 10:
                    return index
                else:
                    if card_val[actionList[index][1]] == curVal + 1:
                        return index

            else:
                index = normal(pair_actionList, pair_member, rank_card)
                if index != -1:
                    return index
                else:
                    return 0
        else:
            index = normal(pair_actionList, pair_member,rank_card)
            if index!=-1:
                return index
            else:
                if pass_num >= 5 or my_pass_num>=3:
                    index = special(pair_actionList,bomb_member,straight_member,rank_card)
                    if index != -1:
                        return index
                cur_bomb_num = cal_bomb_num(sorted_cards, handcards, rank_card)
                if curVal >= max_val and numofgreaterPos >= 15 and cur_bomb_num>1:
                    p = random()
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if p > 0.5:
                        if index != -1:
                            return index
                elif ((curVal >= 14 or curVal>=max_val-2) and numofgreaterPos <= 15) or pass_num >= 6 or my_pass_num>=5:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index!=-1:
                        return index
                    else:
                        return 0


        return 0

    def ThreeWithTwo(self, actionList, curAction,rank_card, handcards, numofplayers,
                    rest_cards, card_val,myPos,greaterPos,pass_num,my_pass_num):

        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]
        numofpre = numofplayers[(myPos-1)%4]

        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        three2_actionList = []
        bomb_actionList = []
        tag = 0

        for action in actionList[1:]:
            tag += 1
            if (action[0] == 'ThreeWithTwo'):
                three2_actionList.append((tag, action))
            else:
                bomb_actionList.append((tag, action))

        curVal = card_val[curAction[1]]
        max_val = 0
        for cards in rest_cards[::-1]:
            if len(cards) >=3:
                max_val = card_val[cards[0][-1]]
                break

        if numofnext == 0:
            numofnext = numofplayers[(myPos-1)%4]

        if numofnext <= 7 or (numofpre <= 7 and numofpre>=1):
            if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
                return 0
            if (myPos + 2) % 4 == greaterPos and curVal >= 11 and numofnext != 5:
                return 0

            three2_sorted = sorted(three2_actionList,key=lambda item:card_val[item[1][1]],reverse=True)
            for action in three2_sorted:
                index = action[0]
                action = action[1]
                trip = action[2][0]
                pair = action[2][3]
                if trip in trip_member and pair in pair_member and rank_card not in action[2] and card_val[pair[1]]<=13:
                    return index

            for action in three2_sorted:
                index = action[0]
                action = action[1]
                trip = action[2][0]
                pair = action[2][3]
                if trip in trip_member and pair in trip_member and rank_card not in action[2] and card_val[pair[1]] >=10:
                    return index

            index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
            if index != -1:
                return index
            for action in three2_sorted:
                index = action[0]
                action = action[1]
                trip = action[2][0]
                pair = action[2][3]
                if trip in pair_member and pair in pair_member and rank_card in action[2]:
                    return index

        def normal(three2_actionList,trip_member,pair_member,rank_card):
            for action in three2_actionList:
                index = action[0]
                action = action[1]
                trip = action[2][0]
                pair = action[2][3]
                if trip in trip_member and pair in pair_member and rank_card not in action[2] and card_val[pair[-1]]<=13:
                    return index
            return -1

        if (myPos + 2) % 4 == greaterPos:
            if curVal >= 14 or curVal >= max_val-2:
                return 0
            elif numoffri <=5 :
                index = normal(three2_actionList, trip_member,pair_member,rank_card)
                if index == -1:
                    return 0
                if curVal <= 10:
                    return index
                else:
                    if card_val[actionList[index][1]] == curVal + 1:
                        return index
            else:
                index = normal(three2_actionList,trip_member,pair_member,rank_card)
                if index!=-1:
                    return index
                else:
                    return 0
        else:
            index = normal(three2_actionList, trip_member, pair_member, rank_card)
            if index != -1:
                return index
            else:
                if curVal>=max_val and numofgreaterPos >= 15:
                    p = random()
                    if p>0.5:
                        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                        if index != -1:
                            return index
                if ((curVal>=12 or curVal>=max_val-2) and numofgreaterPos<=15) or pass_num >= 5 or my_pass_num>=3:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index!=-1:
                        return index
                    else:
                        return 0
        return 0

    def Trips(self,actionList,curAction,rank_card,handcards,numofplayers,rest_cards,card_val,myPos,greaterPos,pass_num,my_pass_num):

        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]
        numofpre = numofplayers[(myPos-1)%4]

        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        trip_actionList = []
        bomb_actionList = []
        tag = 0
        for action in actionList[1:]:
            tag += 1
            if action[0] == 'Trips':
                trip_actionList.append((tag, action))
            else:
                bomb_actionList.append((tag, action))

        curVal = card_val[curAction[1]]
        rest_cards = rest_cards[::-1]
        max_val = 0
        for cards in rest_cards:
            if len(cards) >= 3:
                max_val = card_val[cards[0][-1]]
                break

        if numofnext == 0:
            numofnext = numofplayers[(myPos-1)%4]

        if numofnext <= 6 or (numofpre <= 5 and numofpre>=1):
            if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
                return 0
            if (myPos + 2) % 4 == greaterPos and curVal >= 12 and numofnext != 3:
                return 0

            for action in trip_actionList:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val and action[2][0] in trip_member and action[2] and rank_card not in action[2]:
                    return Index

            index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
            if index != -1:
                return index

            for action in trip_actionList[::-1]:
                Index = action[0]
                action = action[1]
                if card_val[action[1]] >= max_val-2 and action[2][0] in trip_member and rank_card not in action[2]:
                    if is_inStraight(action,straight_member):
                        continue
                    return Index
            max_match = -1
            max_match_index = -1
            for action in trip_actionList:
                index = action[0]
                action = action[1]
                if rank_card in action[2] and card_val[action[1]] > max_match and action[2][0] not in bomb_member:
                    if is_inStraight(action,straight_member):
                        continue
                    max_match = card_val[action[1]]
                    max_match_index = index
            if max_match_index!=-1:
                return max_match_index

        def normal(trip_actionList,trip_member,rank_card):
            for action in trip_actionList:
                Index = action[0]
                action = action[1]
                if action[2][0] in trip_member and rank_card not in action[2]:
                    return Index
            return -1

        if (myPos+2)%4 == greaterPos:
            if curVal >= 13 or curVal>=max_val-2:
                return 0
            elif numoffri <=4 :
                index = normal(trip_actionList,trip_member, rank_card)
                if index == -1:
                    return 0
                if curVal <= 10:
                    return index
                else:
                    if card_val[actionList[index][1]] == curVal + 1:
                        return index
            else:
                index = normal(trip_actionList,trip_member,rank_card)
                if index!=-1:
                    return index
                else:
                    return 0
        else:
            index = normal(trip_actionList,trip_member, rank_card)
            if index!=-1:
                return index
            else:
                if curVal >= max_val and numofgreaterPos>=15:
                    p = random()
                    if p>0.5:
                        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                        if index != -1:
                            return index
                if ((curVal >= 12 or curVal>=max_val-2) and numofgreaterPos <=15) or pass_num >= 5 or my_pass_num>=3:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index !=-1:
                        return index

        return 0

    def ThreePair(self, actionList,curAction,rank_card, handcards, numofplayers,rest_cards, card_val,myPos,greaterPos,pass_num,my_pass_num):

        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]
        numofpre = numofplayers[(myPos-1)%4]
        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        card_origin = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13}
        card_val['A'] = 1
        card_val[rank_card[1]] = card_origin[rank_card[1]]

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        pair3_actionList = []
        bomb_actionList = []

        tag = 0
        for action in actionList[1:]:
            tag += 1
            if (action[0] == 'ThreePair'):
                pair3_actionList.append((tag, action))
            else :
                bomb_actionList.append((tag, action))

        curVal = card_val[curAction[1]]
        max_val = 0
        val_list = []
        for cards in rest_cards:
            if len(cards)>=2:
                val_list.append(card_val[cards[0][1]])
        val_list = sorted(val_list)

        for i in range(0,len(val_list)):
            if i>=len(val_list)-2:
                break
            if (val_list[i]+1 == val_list[i+1] and val_list[i]+2 == val_list[i+2]):
                max_val = max(max_val,val_list[i])

        if len(val_list)>=3 and (val_list[0] ==1 and val_list[-2]==12 and val_list[-1] == 13):
            max_val = 12

        def normal(pair3_actionList,pair_member,rank_card):
            for action in pair3_actionList:
                index = action[0]
                action = action[1]
                first = action[2][0]
                mid = action[2][2]
                last = action[2][4]
                if first in pair_member and mid in pair_member and last in pair_member and rank_card not in action[2]:
                    return index
            return -1

        def special(pair3_actionList,trip_member,rank_card):
            for action in pair3_actionList:
                index = action[0]
                action = action[1]
                first = action[2][0]
                mid = action[2][2]
                last = action[2][4]
                if rank_card in action[2]:
                    continue
                if first in pair_member and mid in pair_member and last in trip_member:
                     return index
                if first in pair_member and mid in trip_member and last in pair_member:
                    return index
                if first in trip_member and mid in pair_member and last in pair_member:
                    return index
            return -1

        def match_rank_card(pair3_actionList,rank_card,pair_member):
            for action in pair3_actionList:
                index = action[0]
                action = action[1]
                first = action[2][1]
                mid = action[2][3]
                last = action[2][5]
                if first == rank_card and mid in pair_member and last in pair_member:
                     return index
                if first in pair_member and mid == rank_card and last in pair_member:
                    return index
                if first in pair_member and mid == rank_card and last in pair_member:
                    return index
            return -1

        if (myPos + 2) % 4 == greaterPos:
            if curVal >= 10 or curVal>=max_val-2:
                return 0
            elif numoffri <=4:
                index = normal(pair3_actionList, pair_member, rank_card)
                if index == -1:
                    return 0
                if curVal <= 7:
                    return index
                else:
                    if card_val[actionList[index][1]] == curVal + 1:
                        return index
            else:
                index = normal(pair3_actionList,pair_member,rank_card)
                if index!=-1:
                    return index
                else:
                    return 0
        else:
            index = normal(pair3_actionList, pair_member, rank_card)
            if index != -1:
                return index
            else:
                index = special(pair3_actionList,trip_member,rank_card)
                if index!=-1:
                    return index
                if len(trip_member)==0 and rank_card in handcards:
                    index = match_rank_card(pair3_actionList,rank_card,pair_member)
                    if index!=-1:
                        return index
                if curVal >= max_val and numofgreaterPos>=15:
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if index != -1:
                        return index
                elif ((curVal >= 10 or curVal>=max_val-2) and numofgreaterPos<=15) or pass_num >= 5  or my_pass_num >= 3:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index!=-1:
                        return index
                    else:
                        return 0

        return 0

    def Straight(self,actionList,curAction,rank_card,handcards,numofplayers,card_val,pass_num,my_pass_num,myPos,greaterPos):
        numofnext = numofplayers[(myPos+1)%4]
        numofpre = numofplayers[(myPos - 1) % 4]
        if numofnext == 0:
            numofnext = numofplayers[(myPos-1)%4]

        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        card_origin = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13, "R": 14, "B": 15}
        card_val['A'] = 1
        card_val[rank_card[1]] = card_origin[rank_card[1]]

        curVal = card_val[curAction[1]]

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        straight_actionList = []
        bomb_actionList = []
        tag = 0
        for action in actionList[1:]:
            tag += 1
            if action[0] == 'Straight':
                straight_actionList.append((tag, action))
            else:
                bomb_actionList.append((tag, action))

        if len(sorted_cards["Straight"])>0:
            curStraight = sorted_cards["Straight"][0][0][1]
            for action in straight_actionList:
                Index = action[0]
                action = action[1]
                if curStraight == action[1] and rank_card not in action[2]:
                    if (myPos+2)%4==greaterPos:
                        if curVal<=7 or card_val[curStraight]-curVal<=2:
                            return Index
                    else:
                        return Index
        elif (myPos+2)!=greaterPos:
            for action in straight_actionList:
                Index = action[0]
                action = action[1]
                if rank_card in action[2] and len(trip_member)==0:
                    if len(set(action[2]).intersection(set(bomb_member)))!=0:
                        continue
                    if is_inStraight(action, straight_member):
                        continue
                    new_handcards = []
                    for card in handcards:
                        if card not in action[2]:
                            new_handcards.append(card)

                    new_card_val = copy.deepcopy(card_val)
                    new_card_val['A']=14
                    new_card_val[rank_card[1]]=15
                    originSinglenum = len(single_member)
                    new_sorted_cards,_ = combine_handcards(new_handcards,rank_card,new_card_val)
                    curSinglenum = len(new_sorted_cards["Single"])
                    if curSinglenum<=originSinglenum:
                        return Index

            if (numofnext <= 15 or curVal >= 9) or numofnext<=10 or pass_num >= 5 or my_pass_num>=3 or numofpre<=5:
                index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                if index != -1:
                    return index

        return 0

    def TwoTrips(self, actionList, curAction,rank_card,handcards,numofplayers, rest_cards, card_val,myPos,greaterPos,pass_num,my_pass_num):

        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        numoffri = numofplayers[(myPos + 2) % 4]

        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1],card_val)

        card_origin = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13}
        card_val['A'] = 1
        card_val[rank_card[1]] = card_origin[rank_card[1]]

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb

        twoTripsList = []
        bomb_actionList = []
        tag = 0

        for action in actionList[1:]:
            tag += 1
            if (action[0] == "TwoTrips"):
                twoTripsList.append((tag, action))
            else :
                bomb_actionList.append((tag, action))

        curVal = card_val[curAction[1]]
        max_val = 0
        val_list = []
        for cards in rest_cards:
            if len(cards) >= 3:
                val_list.append(card_val[cards[0][1]])
        val_list = sorted(val_list)
        for i in range(0,len(val_list)):
            if (i >= len(val_list)-1):
                break
            if (val_list[i]+1 == val_list[i+1]):
                max_val = max(max_val,val_list[i])
        if len(val_list)>=2 and val_list[0] == 1 and val_list[-1]==13:
            max_val = 13

        def normal(twoTripsList,trip_member,rank_card):
            for action in twoTripsList:
                index = action[0]
                action = action[1]
                first = action[2][0]
                last = action[2][3]
                if first in trip_member and last in trip_member and rank_card not in action[2]:
                    return index
            return -1

        if (myPos + 2) % 4 == greaterPos:
            if curVal >= 10 or curVal>=max_val-2:
                return 0
            elif numoffri <=4:
                index = normal(twoTripsList, trip_member, rank_card)
                if index == -1:
                    return 0
                if curVal <= 10:
                    return index
                else:
                    if card_val[actionList[index][1]] == curVal + 1:
                        return index
            else:
                index = normal(twoTripsList,trip_member,rank_card)
                if index!=-1:
                    return index
                else:
                    return 0
        else:
            index = normal(twoTripsList, trip_member, rank_card)
            if index != -1:
                return index
            else:
                if curVal >= max_val and numofgreaterPos >= 15:
                    p = random()
                    if p>0.5:
                        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                        if index != -1:
                            return index
                if ((curVal>=10 or curVal>=max_val-2) and numofgreaterPos<=15)  or pass_num>=5 or my_pass_num >= 3:
                    index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
                    if index!=-1:
                        return index
                    else:
                        return 0
        return 0
    def Bomb(self,actionList,curAction,rank_card,handcards,numofplayers,rest_cards,card_val,myPos,greaterPos):
        numofnext = numofplayers[(myPos + 1) % 4]
        numofgreaterPos = numofplayers[greaterPos]
        if (myPos + 2) % 4 == greaterPos:
            return 0

        sorted_cards, bomb_info = combine_handcards(handcards, rank_card[1],card_val)
        cur_Bomb_num = cal_bomb_num(sorted_cards,handcards,rank_card)

        bomb_member = []
        pair_member = []
        trip_member = []
        single_member = sorted_cards["Single"]
        straight_member = []
        if len(sorted_cards["Straight"]) != 0:
            straight_member += sorted_cards["Straight"][0]
        if len(sorted_cards["StraightFlush"]) != 0:
            straight_member += sorted_cards["StraightFlush"][0]

        for pair in sorted_cards["Pair"]:
            pair_member += pair
        for trip in sorted_cards["Trips"]:
            trip_member += trip
        for bomb in sorted_cards["Bomb"]:
            bomb_member += bomb
        bomb_actionList = []
        tag = 0
        for action in actionList[1:]:
            tag += 1
            bomb_actionList.append((tag, action))
        if cur_Bomb_num >= 3:
            index = choose_bomb(bomb_actionList,handcards,sorted_cards,bomb_info,rank_card,card_val)
            if index!=-1:
                return index
        elif numofgreaterPos <= 18:
            index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
            if index != -1:
                return index

        return 0


    def passive(self,actionList,handcards,rank,curAction,greaterAction,myPos,greaterPos,remaincards,
                numofplayers,pass_num,my_pass_num,remain_cards_classbynum):

        rank_card = 'H' + str(rank)
        restcards = rest_cards(handcards, remaincards, rank)

        card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                          "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17,"JOKER":10000}

        card_value_s2v[rank_card[1]] = 15


        actIndex = 0
        if curAction[0]=="PASS":
            curAction = greaterAction
        print(curAction)
        numofmy = numofplayers[myPos]
        if numofmy <= 10:
            numofnext = numofplayers[(myPos+1)%4]
            actIndex = one_hand(numofmy,numofnext,actionList,myPos,greaterPos,7,
                     restcards,card_value_s2v,rank_card)
            if actIndex!=-1:
                return actIndex

        if curAction[0] == "Single":

            actIndex = self.Single(actionList,curAction,rank_card,handcards,numofplayers,restcards,
                                   card_value_s2v,myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "Pair":
            actIndex = self.Pair(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                                 card_value_s2v, myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "Trips":
            actIndex = self.Trips(actionList,curAction,rank_card,handcards,numofplayers,restcards,
                                  card_value_s2v,myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "ThreeWithTwo":
            actIndex = self.ThreeWithTwo(actionList, curAction,rank_card, handcards, numofplayers,restcards,
                                         card_value_s2v,myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "ThreePair":
            actIndex = self.ThreePair(actionList,curAction,rank_card, handcards, numofplayers,restcards,
                                      card_value_s2v,myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "TwoTrips":
            actIndex = self.TwoTrips(actionList, curAction,rank_card,handcards,numofplayers, restcards,
                                     card_value_s2v,myPos,greaterPos,pass_num,my_pass_num)

        elif curAction[0] == "Straight" :
            actIndex = self.Straight(actionList,curAction,rank_card,handcards,numofplayers,card_value_s2v,pass_num,my_pass_num,myPos,greaterPos)
        elif curAction[0] == "Bomb" or curAction[0] == "StraightFlush":
            actIndex = self.Bomb(actionList,curAction,rank_card,handcards,numofplayers,restcards,
                                 card_value_s2v,myPos,greaterPos)

        return actIndex


    def getlist(self,handcards,rank):
        single_actionlist = []
        pair_actionlist = []
        trips_actionlist = []
        threepair_actionlist = []
        threetwo_actionlist = []
        twotrips_actionlist = []
        straight_actionlist = []

        action2 = "None"
        action3 = "None"

        rank_card = 'H' + str(rank)

        card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                          "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
        card_value_s2v2 = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                           "Q": 12, "K": 13, "B": 16, "R": 17}
        card_value_s2v[rank_card[-1]] = 15
        sorted_cards, bomb_info = combine_handcards(handcards, rank,card_value_s2v)

        def mysort(elem):
            return card_value_s2v[elem[0]]

        def mysort1(elem):
            return card_value_s2v2[elem[0]]

        if sorted_cards["Single"]:
            for singlecard in sorted_cards['Single']:
                single_actionlist.append([singlecard[-1], singlecard])
            single_actionlist.sort(key=mysort)

        if sorted_cards["Pair"]:
            for paircard in sorted_cards['Pair']:
                pair_actionlist.append([paircard[0][-1], paircard])
            pair_actionlist.sort(key=mysort)

        if sorted_cards['Trips']:
            for tripcard in sorted_cards['Trips']:
                trips_actionlist.append([tripcard[0][-1], tripcard])
            trips_actionlist.sort(key=mysort)

        if sorted_cards['Pair'] and sorted_cards['Trips']:
            for tripcard in sorted_cards['Trips']:
                for paircard in sorted_cards['Pair']:
                    threetwo_actionlist.append([tripcard[0][-1], tripcard + paircard])
            threetwo_actionlist.sort(key=mysort)

        if len(sorted_cards['Pair']) >= 3:
            for i in range(len(pair_actionlist) - 2):
                if card_value_s2v[pair_actionlist[i][0]] == card_value_s2v[pair_actionlist[i + 1][0]] - 1 and \
                        card_value_s2v[pair_actionlist[i + 1][0]] == card_value_s2v[pair_actionlist[i + 2][0]] - 1:
                    action2 = pair_actionlist[i][-1] + pair_actionlist[i + 1][-1] + pair_actionlist[i + 2][-1]
                    threepair_actionlist.append([action2[0][-1], action2])
            threepair_actionlist.sort(key=mysort1)

        if len(sorted_cards['Trips']) >= 2:
            for i in range(len(trips_actionlist) - 1):
                if card_value_s2v[trips_actionlist[i][0]] == card_value_s2v[trips_actionlist[i + 1][0]] - 1:
                    action3 = trips_actionlist[i][-1] + trips_actionlist[i + 1][-1]
                    twotrips_actionlist.append([action3[0][-1], action3])
            twotrips_actionlist.sort(key=mysort1)

        if 'Straight' in sorted_cards.keys() and sorted_cards['Straight']:
            for straightcard in sorted_cards['Straight']:
                straight_actionlist.append([straightcard[0][-1], straightcard])
            straight_actionlist.sort(key=mysort1)


        return sorted_cards, single_actionlist, pair_actionlist, trips_actionlist, threepair_actionlist,threetwo_actionlist, twotrips_actionlist, straight_actionlist

    def active(self,actionList,handcards,rank,numofplayers,mypos,remaincards):
        restcards = rest_cards(handcards, remaincards, rank)
        rank_card = 'H' + rank
        numofnext = numofplayers[(mypos + 1) % 4]
        if numofnext == 0:
            numofnext = numofplayers[(mypos - 1) % 4]

        cur = [9,10,9,8,10,10,2]
        card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                          "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
        card_value_s2v2 = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                           "Q": 12, "K": 13, "B": 16, "R": 17}
        card_value_s2v[rank] = 15

        sorted_cards,single_actionlist, pair_actionlist, trips_actionlist, threepair_actionlist,threetwo_actionlist, twotrips_actionlist, straight_actionlist = self.getlist(
            handcards, rank)
        print(len(single_actionlist), len(pair_actionlist), len(trips_actionlist), len(threetwo_actionlist), len(threepair_actionlist), len(twotrips_actionlist), len(straight_actionlist))

        max_val = card_value_s2v[restcards[-1][0][-1]]

        for i in actionList:
            if len(handcards) == len(i[2]):
                return actionList.index(i)

        twohand_candidatelist = []
        def mysort2(elem):
            return elem[1]

        if len(handcards) <= 12:
            for i in range(len(actionList)):
                for j in range(i+1,len(actionList)):
                    if len(actionList[i][-1]) + len(actionList[j][-1]) == len(handcards):
                        combine_list = actionList[i][-1] + actionList[j][-1]
                        if combine_list.sort(key=mysort2) == handcards.sort(key=mysort2):
                            twohand_candidatelist.append((i,j))

        if len(single_actionlist) and card_value_s2v[single_actionlist[0][0]] < cur[0] :
            if numofnext == 1:
                pass
            else:
                return getindex("Single", single_actionlist, actionList)

        if len(threepair_actionlist) or len(twotrips_actionlist):
            index =rankfour(twotrips_actionlist, threepair_actionlist, actionList, cur[1], cur[2])
            if index is None:
                pass
            else:
                return index


        if len(straight_actionlist) and card_value_s2v2[straight_actionlist[0][0]] < cur[4]:
            return getindex("Straight", straight_actionlist, actionList)

        if len(threetwo_actionlist):

            index = rankthree(single_actionlist, pair_actionlist, trips_actionlist, threetwo_actionlist, actionList,numofnext,
                              rank, cur[0], cur[3], cur[4], cur[5], cur[-1])

            if index is None:
                pass
            else:
                return index
        if len(trips_actionlist):
            return rankone(single_actionlist, trips_actionlist, actionList, numofnext, rank)
        if len(pair_actionlist):
            return ranktwo(handcards,single_actionlist,pair_actionlist,trips_actionlist,actionList,numofnext,rank,max_val)
        if len(single_actionlist):
            if numofnext == 1 and len(trips_actionlist) == 0 and len(pair_actionlist) == 0 and rank_card in handcards:
                for i in range(len(actionList)):
                    if actionList[i][0] == 'Pair' and (actionList[i][-1][0] in sorted_cards['Single'] or actionList[i][-1][-1] in sorted_cards['Single']):
                        return i


            if numofnext == 1:
                if len(trips_actionlist) == 0 and len(pair_actionlist) == 0 and rank_card not in handcards:
                    for acti in range(len(actionList)):
                        if len(actionList[acti][-1])>1 and actionList[acti][0]!='Bomb':
                            return acti
                now_max_act_value = 0
                now_max_act_key = 0
                for acti in range(len(actionList)):
                    if actionList[acti][0] == 'Single' and actionList[acti][-1][0] in sorted_cards['Single']:
                        if card_value_s2v[actionList[acti][1]] > now_max_act_value:
                            now_max_act_value = card_value_s2v[actionList[acti][1]]
                            now_max_act_key = acti

                return now_max_act_key

            return getindex("Single", single_actionlist, actionList)
        else:
            return  0

    def back_action(self, msg, mypos, tribute_result):
        rank = msg["curRank"]
        self.action = msg["actionList"]
        handCards = msg["handCards"]
        card_val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                    "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
        card_val[rank] = 15

        def flag_TJQ(handCards_X) -> tuple:
            flag_T = False
            flag_J = False
            flag_Q = False
            for i in range(len(handCards_X)):
                if handCards_X[i][0][-1] == "T":
                    flag_T = True
                if handCards_X[i][0][-1] == "J":
                    flag_J = True
                if handCards_X[i][0][-1] == "Q":
                    flag_Q = True
            return flag_T, flag_J, flag_Q

        def get_card_index(target: str) -> int:
            for i in range(len(self.action)):
                if self.action[i][2][0] == target:
                    return i

        def choose_in_single(single_list) -> str:
            for my_pos in tribute_result:
                if my_pos[1] == mypos:
                    tribute_pos = my_pos[0]

            n = len(single_list)
            if (int(tribute_pos) + int(mypos)) % 2 != 0:
                for card in single_list:
                    if card in ['H5', 'HT']:
                        return card
                    elif card in ['S5', 'C5', 'D5', 'ST', 'CT', 'DT']:
                        return card
                return single_list[randint(0, n - 1)]
            else:
                back_list = []
                for card in single_list:
                    if card[-1] != 'T':
                        if int(card[-1]) < 5:
                            back_list.append(card)
                if back_list:
                    return back_list[randint(0, len(back_list) - 1)]
                return single_list[randint(0, n - 1)]

        def choose_in_pair(pair_list, pair_list_from_handcards) -> str:
            val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
            if len(pair_list) < 3:
                return pair_list[0][0]
            for i in range(len(pair_list)):
                flag = False
                if i >= 2:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i - 2][0][-1], pair_list[i - 1][0][-1], \
                                                                      pair_list[i][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if 1 <= i <= len(pair_list) - 2:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i - 1][0][-1], pair_list[i][0][-1], \
                                                                      pair_list[i + 1][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if i <= len(pair_list) - 3:
                    pair_first_val, pair_second_val, pair_third_val = pair_list[i][0][-1], pair_list[i + 1][0][-1], \
                                                                      pair_list[i + 2][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                            val_dict[pair_third_val] - 1:
                        flag = True
                if pair_list[i][0][-1] == '9':
                    flag_T, flag_J, flag_Q = flag_TJQ(pair_list_from_handcards)
                    if flag_T and flag_J:
                        flag = True
                if pair_list[i][0][-1] == 'T':
                    flag_T, flag_J, flag_Q = flag_TJQ(pair_list_from_handcards)
                    if flag_J and flag_Q:
                        flag = True
                if flag:
                    continue
                else:
                    return pair_list[i][0]
            return pair_list[0][0]

        def choose_in_trips(trips_list, trips_list_from_handcards) -> str:
            val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
            if len(trips_list) < 2:
                return trips_list[0][0]
            for i in range(len(trips_list)):
                flag = False
                if i >= 1:
                    pair_first_val, pair_second_val = trips_list[i - 1][0][-1], trips_list[i][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1:
                        flag = True
                if i <= len(trips_list) - 2:
                    pair_first_val, pair_second_val = trips_list[i][0][-1], trips_list[i + 1][0][-1]
                    if val_dict[pair_first_val] == val_dict[pair_second_val] - 1:
                        flag = True
                if trips_list[i][0][-1] == 'T':
                    flag_T, flag_J, flag_Q = flag_TJQ(trips_list_from_handcards)
                    if flag_J:
                        flag = True
                if flag:
                    continue
                else:
                    return trips_list[i][0]
            return trips_list[0][0]

        def choose_in_bomb(bomb_list, bomb_info) -> str:

            def get_card_from_bomb(bomb_list, key):
                for bomb in bomb_list:
                    for card in bomb:
                        if card[-1] == key:
                            return card

            for key, value in bomb_info:
                if value > 4:
                    return get_card_from_bomb(bomb_list, key)
            return bomb_list[0][0]

        combined_handcards, handCards_bomb_info = combine_handcards(handCards, rank, card_val)  # 将手牌组合起来

        combined_temp = {"Single": [], "Trips": [], "Pair": [], "Bomb": []}
        temp_bomb_info = {}
        for card in combined_handcards["Single"]:
            if card_val[card[-1]] <= 10:
                combined_temp["Single"].append(card)
        for trips_card in combined_handcards["Trips"]:
            if card_val[trips_card[0][-1]] <= 10:
                combined_temp["Trips"].append(trips_card)
        for pair_card in combined_handcards["Pair"]:
            if card_val[pair_card[0][-1]] <= 10:
                combined_temp["Pair"].append(pair_card)
        for bomb_card in combined_handcards["Bomb"]:
            if card_val[bomb_card[0][-1]] <= 10:
                combined_temp["Bomb"].append(bomb_card)
        for key, values in handCards_bomb_info.items():
            if card_val[key] <= 10:
                temp_bomb_info[key] = values

        card = None
        if combined_temp["Single"]:
            card = choose_in_single(combined_temp["Single"])
        elif combined_temp["Trips"]:
            card = choose_in_trips(combined_temp["Trips"], combined_handcards["Trips"])
        elif combined_temp["Pair"]:
            card = choose_in_pair(combined_temp["Pair"], combined_handcards["Pair"])
        elif combined_temp["Bomb"]:
            card = choose_in_bomb(combined_temp["Bomb"], temp_bomb_info)
        else:
            temp = []
            for handCard in handCards:
                if card_val[handCard[-1]] <= 10:
                    temp.append(handCard)
            card = temp[randint(0, len(temp) - 1)]
        return get_card_index(card)
    def tribute(self,actionList,rank):

        rank_card = 'H'+rank
        first_action = actionList[0]
        if rank_card in first_action[2]:
            return 1
        else:
            return 0

    def rule_parse(self,msg,mypos,remaincards,history,remain_cards_classbynum,pass_num,my_pass_num,tribute_result):
        self.action = msg["actionList"]
        if len(self.action) == 1:
            return 0
        if msg["stage"] == "play" and msg["greaterPos"] != mypos and msg["curPos"] != -1:  # 被动出牌
            # try:

            numofplayers = [history['0']["remain"],history['1']["remain"],history['2']["remain"],history['3']["remain"]]
            numofnext = numofplayers[(mypos + 1) % 4]
            if numofnext != 0:
                print("下家还有{}张牌".format(numofnext))
            else:
                numofpre = numofplayers[(mypos - 1) % 4]
                print("下家已完牌，上家还有{}张牌".format(numofpre))
            # print(msg['curAction'])
            self.act = self.passive(self.action, msg["handCards"], msg["curRank"], msg['curAction'],msg["greaterAction"],mypos,
                                    msg["greaterPos"],remaincards, numofplayers,pass_num,my_pass_num,remain_cards_classbynum)
            # except Exception as e:
            #     self.ger.info(str(e))
            #     print(str(e))
            #     self.act = 1

        elif msg["stage"] == "play" and (msg["greaterPos"] == -1 or msg["curPos"] == -1):  # 第一句情况以及主动情况
            # try:
            numofplayers = [history['0']["remain"], history['1']["remain"], history['2']["remain"],
                            history['3']["remain"]]
            numofnext = numofplayers[(mypos + 1) % 4]
            if numofnext != 0:
                print("下家还有{}张牌".format(numofnext))
            else:
                numofpre = numofplayers[(mypos - 1) % 4]
            self.act = self.active(self.action, msg["handCards"], msg["curRank"],numofplayers,mypos,remaincards)
            # except Exception as e:
            #     self.logger.info(str(e))
            #     self.act = 1
        elif msg["stage"] == "back":
            # try:
            self.act = self.back_action(msg,mypos,tribute_result)
            # except Exception as e:
            #     self.logger.info(str(e))
            #     print(e)
            #     self.act = 1
        elif msg["stage"] == "tribute":
            # try:
            self.act = self.tribute(self.action,msg["curRank"])
            # except Exception as e:
            #     print(e)
            #     self.logger.info(str(e))
            #     self.act = 0
        else:
            self.act_range = msg["indexRange"]
            self.act = randint(0, self.act_range)

        return self.act

    def random_parse(self,msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        return randint(0,self.act_range)