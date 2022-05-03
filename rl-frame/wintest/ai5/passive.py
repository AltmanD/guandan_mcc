#!/usr/bin/env python
# encoding: utf-8
"""
@author:Naynix
@contact: naynix@qq.com
@file: passive.py
@time: 2020/10/26 21:01
"""
import copy
import logging
from random import randint, random

from utils.utils import *


def Single( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos,
           pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]
    numofmy = numofplayers[myPos]
    numofpre = numofplayers[(myPos - 1) % 4]

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[1], card_val)

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

    tag = 0
    single_actionList = []
    bomb_actionList = []
    for action in actionList[1:]:
        tag += 1
        if action[0] == 'Single':
            single_actionList.append((tag, action))
        else:
            bomb_actionList.append((tag, action))

    curVal = card_val[curAction[1]]

    max_val = card_val[rest_cards[-1][0][1]]

    if numofnext == 0:
        numofnext = numofplayers[(myPos - 1) % 4]

    if numofnext <= 4 or (numofpre <= 3 and numofpre >= 1):


        if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
            return 0
        if (myPos + 2) % 4 == greaterPos and curVal >= 15 and numofnext != 1:
            return 0

        for action in single_actionList:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val and action[2][0] in single_member and rank_card not in action[2]:
                return Index

        for action in single_actionList:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val and action[2][0] not in bomb_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
                    continue
                return Index

        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
        if index != -1:
            return index

        for action in single_actionList:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val - 2 and action[2][0] not in bomb_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
                    continue
                return Index

        for action in single_actionList:
            Index = action[0]
            action = action[1]
            if rank_card in action[2] and (len(sorted_cards["Pair"]) < 3 or numofnext == 1):
                return Index

    def normal(single_actionList, single_member, rank_card):
        for action in single_actionList:
            Index = action[0]
            action = action[1]
            if (action[2][0] in single_member or card_val[action[1]] >= 15) and rank_card not in action[2]:
                return Index
        return -1

    def special(single_actionList, bomb_member, straight_member, rank_card):
        for action in single_actionList[::-1]:
            Index = action[0]
            action = action[1]
            if action[2][0] not in bomb_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
                    continue
                return Index
        return -1

    if (myPos + 2) % 4 == greaterPos:
        if curVal >= 14 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 4:
            index = normal(single_actionList, single_member, rank_card)
            if index == -1:
                return 0
            if curVal <= 10:
                return index
            else:
                print(index)
                if card_val[actionList[index][1]] == curVal + 1:
                    return index
        else:
            index = normal(single_actionList, single_member, rank_card)
            if index != -1:
                return index
            else:
                return 0
    else:
        index = normal(single_actionList, single_member, rank_card)
        if index != -1:
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
            elif ((curVal >= 15 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 7 or my_pass_num >= 5:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
                else:
                    return 0

    return 0


def Pair( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos,
         pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]
    numofpre = numofplayers[(myPos - 1) % 4]
    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)

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
            pair_actionList.append((tag, action))
        else:
            bomb_actionList.append((tag, action))

    curVal = card_val[curAction[1]]
    rest_cards = rest_cards[::-1]
    max_val = 0
    for cards in rest_cards:
        if len(cards) >= 2:
            max_val = card_val[cards[0][1]]
            break

    if numofnext == 0:
        numofnext = numofplayers[(myPos - 1) % 4]

    if numofnext <= 4 or (numofpre <= 4 and numofpre >= 1):

        if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
            return 0
        if (myPos + 2) % 4 == greaterPos and curVal >= 12 and numofnext != 2:
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
                if is_inStraight(action, straight_member):
                    continue
                return Index

        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
        if index != -1:
            return index

        for action in pair_actionList[::-1]:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val - 2 and action[2][0] not in bomb_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
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
        if max_match_index != -1 and max_match >= max_val - 2:
            return max_match_index


    def normal(pair_actionList, pair_member, rank_card):
        for action in pair_actionList:
            Index = action[0]
            action = action[1]
            if (action[2][0] in pair_member or action[1] == rank_card[1]) and rank_card not in action[2]:
                return Index

        return -1

    def special(pair_actionList, bomb_member, straight_member, rank_card):
        for action in pair_actionList[::-1]:
            Index = action[0]
            action = action[1]

            if action[2][0] not in bomb_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
                    continue
                return Index
        return -1

    if (myPos + 2) % 4 == greaterPos:
        if curVal >= 13 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 4:
            index = normal(pair_actionList, pair_member, rank_card)
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
        index = normal(pair_actionList, pair_member, rank_card)
        if index != -1:
            return index
        else:
            if pass_num >= 5 or my_pass_num >= 3:
                index = special(pair_actionList, bomb_member, straight_member, rank_card)
                if index != -1:
                    return index
            cur_bomb_num = cal_bomb_num(sorted_cards, handcards, rank_card)
            if curVal >= max_val and numofgreaterPos >= 15 and cur_bomb_num > 1:
                p = random()
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if p > 0.5:
                    if index != -1:
                        return index
            elif ((curVal >= 14 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 6 or my_pass_num >= 5:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
                else:
                    return 0

    return 0


def ThreeWithTwo( actionList, curAction, rank_card, handcards, numofplayers,
                 rest_cards, card_val, myPos, greaterPos, pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]
    numofpre = numofplayers[(myPos - 1) % 4]

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)

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

    curVal = card_val[curAction[1]]  # 当前牌的值
    max_val = 0
    for cards in rest_cards[::-1]:
        if len(cards) >= 3:
            max_val = card_val[cards[0][-1]]  # 另外三方的可能最大值
            break

    if numofnext == 0:
        numofnext = numofplayers[(myPos - 1) % 4]

    if numofnext <= 7 or (numofpre <= 7 and numofpre >= 1):

        if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
            return 0
        if (myPos + 2) % 4 == greaterPos and curVal >= 11 and numofnext != 5:
            return 0

        three2_sorted = sorted(three2_actionList, key=lambda item: card_val[item[1][1]], reverse=True)
        for action in three2_sorted:
            index = action[0]
            action = action[1]
            trip = action[2][0]
            pair = action[2][3]
            if trip in trip_member and pair in pair_member and rank_card not in action[2] and card_val[pair[1]] <= 13:
                return index

        for action in three2_sorted:
            index = action[0]
            action = action[1]
            trip = action[2][0]
            pair = action[2][3]
            if trip in trip_member and pair in trip_member and rank_card not in action[2] and card_val[pair[1]] >= 10:
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

    def normal(three2_actionList, trip_member, pair_member, rank_card):
        for action in three2_actionList:
            index = action[0]
            action = action[1]
            trip = action[2][0]
            pair = action[2][3]
            if trip in trip_member and pair in pair_member and rank_card not in action[2] and card_val[pair[-1]] <= 13:
                return index
        return -1

    if (myPos + 2) % 4 == greaterPos:
        if curVal >= 14 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 5:
            index = normal(three2_actionList, trip_member, pair_member, rank_card)
            if index == -1:
                return 0
            if curVal <= 10:
                return index
            else:
                if card_val[actionList[index][1]] == curVal + 1:
                    return index
        else:
            index = normal(three2_actionList, trip_member, pair_member, rank_card)
            if index != -1:
                return index
            else:
                return 0
    else:
        index = normal(three2_actionList, trip_member, pair_member, rank_card)
        if index != -1:
            return index
        else:
            if curVal >= max_val and numofgreaterPos >= 15:
                p = random()
                if p > 0.5:
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if index != -1:
                        return index
            if ((curVal >= 12 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 5 or my_pass_num >= 3:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
                else:
                    return 0
    return 0


def Trips( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos,
          pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]
    numofpre = numofplayers[(myPos - 1) % 4]

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)

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
        numofnext = numofplayers[(myPos - 1) % 4]

    if numofnext <= 6 or (numofpre <= 5 and numofpre >= 1):

        if (myPos + 2) % 4 == greaterPos and curVal >= max_val:
            return 0
        if (myPos + 2) % 4 == greaterPos and curVal >= 12 and numofnext != 3:
            return 0

        for action in trip_actionList:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val and action[2][0] in trip_member and action[2] and rank_card not in action[
                2]:
                return Index

        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
        if index != -1:
            return index

        for action in trip_actionList[::-1]:
            Index = action[0]
            action = action[1]
            if card_val[action[1]] >= max_val - 2 and action[2][0] in trip_member and rank_card not in action[2]:
                if is_inStraight(action, straight_member):
                    continue
                return Index
        max_match = -1
        max_match_index = -1
        for action in trip_actionList:
            index = action[0]
            action = action[1]
            if rank_card in action[2] and card_val[action[1]] > max_match and action[2][0] not in bomb_member:
                if is_inStraight(action, straight_member):
                    continue
                max_match = card_val[action[1]]
                max_match_index = index
        if max_match_index != -1:
            return max_match_index

    def normal(trip_actionList, trip_member, rank_card):
        for action in trip_actionList:
            Index = action[0]
            action = action[1]
            if action[2][0] in trip_member and rank_card not in action[2]:
                return Index
        return -1

    if (myPos + 2) % 4 == greaterPos:
        if curVal >= 13 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 4:
            index = normal(trip_actionList, trip_member, rank_card)
            if index == -1:
                return 0
            if curVal <= 10:
                return index
            else:
                if card_val[actionList[index][1]] == curVal + 1:
                    return index
        else:
            index = normal(trip_actionList, trip_member, rank_card)
            if index != -1:
                return index
            else:
                return 0
    else:
        index = normal(trip_actionList, trip_member, rank_card)
        if index != -1:
            return index
        else:
            if curVal >= max_val and numofgreaterPos >= 15:
                p = random()
                if p > 0.5:
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if index != -1:
                        return index
            if ((curVal >= 12 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 5 or my_pass_num >= 3:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index

    return 0

def ThreePair( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos,
              pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]
    numofpre = numofplayers[(myPos - 1) % 4]
    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)


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
        else:
            bomb_actionList.append((tag, action))

    curVal = card_val[curAction[1]]
    max_val = 0
    val_list = []
    for cards in rest_cards:
        if len(cards) >= 2:
            val_list.append(card_val[cards[0][1]])
    val_list = sorted(val_list)

    for i in range(0, len(val_list)):
        if i >= len(val_list) - 2:
            break
        if (val_list[i] + 1 == val_list[i + 1] and val_list[i] + 2 == val_list[i + 2]):
            max_val = max(max_val, val_list[i])

    if len(val_list) >= 3 and (val_list[0] == 1 and val_list[-2] == 12 and val_list[-1] == 13):
        max_val = 12


    def normal(pair3_actionList, pair_member, rank_card):
        for action in pair3_actionList:
            index = action[0]
            action = action[1]
            first = action[2][0]
            mid = action[2][2]
            last = action[2][4]

            if first in pair_member and mid in pair_member and last in pair_member and rank_card not in action[2]:
                return index
        return -1

    def special(pair3_actionList, trip_member, rank_card):
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

    def match_rank_card(pair3_actionList, rank_card, pair_member):
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
        if curVal >= 10 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 4:
            index = normal(pair3_actionList, pair_member, rank_card)
            if index == -1:
                return 0
            if curVal <= 7:
                return index
            else:
                if card_val[actionList[index][1]] == curVal + 1:
                    return index
        else:
            index = normal(pair3_actionList, pair_member, rank_card)
            if index != -1:
                return index
            else:
                return 0
    else:
        index = normal(pair3_actionList, pair_member, rank_card)
        if index != -1:
            return index
        else:
            index = special(pair3_actionList, trip_member, rank_card)
            if index != -1:
                return index
            if len(trip_member) == 0 and rank_card in handcards:
                index = match_rank_card(pair3_actionList, rank_card, pair_member)
                if index != -1:
                    return index
            if curVal >= max_val and numofgreaterPos >= 15:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
            elif ((curVal >= 10 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 5 or my_pass_num >= 3:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
                else:
                    return 0
    return 0


def Straight( actionList, curAction, rank_card, handcards, numofplayers, card_val, pass_num, my_pass_num, myPos,
             greaterPos):


    numofnext = numofplayers[(myPos + 1) % 4]
    numofpre = numofplayers[(myPos - 1) % 4]
    if numofnext == 0:
        numofnext = numofplayers[(myPos - 1) % 4]

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)

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

    if len(sorted_cards["Straight"]) > 0:
        curStraight = sorted_cards["Straight"][0][0][1]
        for action in straight_actionList:
            Index = action[0]
            action = action[1]
            if curStraight == action[1] and rank_card not in action[2]:
                if (myPos + 2) % 4 == greaterPos:
                    if curVal <= 7 or card_val[curStraight] - curVal <= 2:
                        return Index
                else:
                    return Index
    elif (myPos + 2) != greaterPos:
        for action in straight_actionList:
            Index = action[0]
            action = action[1]
            if rank_card in action[2] and len(trip_member) == 0:
                if len(set(action[2]).intersection(set(bomb_member))) != 0:
                    continue
                if is_inStraight(action, straight_member):
                    continue
                new_handcards = []
                for card in handcards:
                    if card not in action[2]:
                        new_handcards.append(card)

                new_card_val = copy.deepcopy(card_val)
                new_card_val['A'] = 14
                new_card_val[rank_card[1]] = 15
                originSinglenum = len(single_member)
                new_sorted_cards, _ = combine_handcards(new_handcards, rank_card, new_card_val)
                curSinglenum = len(new_sorted_cards["Single"])
                if curSinglenum <= originSinglenum:
                    return Index

        if (numofnext <= 15 or curVal >= 9) or numofnext <= 10 or pass_num >= 5 or my_pass_num >= 3 or (
                numofpre <= 5 and numofpre >= 1):
            index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
            if index != -1:
                return index
    return 0

def TwoTrips( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos,
             pass_num, my_pass_num):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    numoffri = numofplayers[(myPos + 2) % 4]

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[-1], card_val)
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
        else:
            bomb_actionList.append((tag, action))

    curVal = card_val[curAction[1]]
    max_val = 0
    val_list = []
    for cards in rest_cards:
        if len(cards) >= 3:
            val_list.append(card_val[cards[0][1]])
    val_list = sorted(val_list)
    for i in range(0, len(val_list)):
        if (i >= len(val_list) - 1):
            break
        if (val_list[i] + 1 == val_list[i + 1]):
            max_val = max(max_val, val_list[i])
    if len(val_list) >= 2 and val_list[0] == 1 and val_list[-1] == 13:
        max_val = 13


    def normal(twoTripsList, trip_member, rank_card):
        for action in twoTripsList:
            index = action[0]
            action = action[1]
            first = action[2][0]
            last = action[2][3]
            if first in trip_member and last in trip_member and rank_card not in action[2]:
                return index
        return -1

    if (myPos + 2) % 4 == greaterPos:
        if curVal >= 10 or curVal >= max_val - 2:
            return 0
        elif numoffri <= 4:
            index = normal(twoTripsList, trip_member, rank_card)
            if index == -1:
                return 0
            if curVal <= 10:
                return index
            else:
                if card_val[actionList[index][1]] == curVal + 1:
                    return index
        else:
            index = normal(twoTripsList, trip_member, rank_card)
            if index != -1:
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
                if p > 0.5:
                    index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                    if index != -1:
                        return index
            if ((curVal >= 10 or curVal >= max_val - 2) and numofgreaterPos <= 15) or pass_num >= 5 or my_pass_num >= 3:
                index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
                if index != -1:
                    return index
                else:
                    return 0
    return 0

def Bomb( actionList, curAction, rank_card, handcards, numofplayers, rest_cards, card_val, myPos, greaterPos):
    numofnext = numofplayers[(myPos + 1) % 4]
    numofgreaterPos = numofplayers[greaterPos]
    if (myPos + 2) % 4 == greaterPos:
        return 0

    sorted_cards, bomb_info = combine_handcards(handcards, rank_card[1], card_val)
    cur_Bomb_num = cal_bomb_num(sorted_cards, handcards, rank_card)

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
        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
        if index != -1:
            return index
    elif numofgreaterPos <= 18:
        index = choose_bomb(bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val)
        if index != -1:
            return index
    return 0

def passive( actionList, handcards, rank, curAction, greaterAction, myPos, greaterPos, remaincards,
            numofplayers, pass_num, my_pass_num, remain_cards_classbynum):
    rank_card = 'H' + str(rank)
    restcards = rest_cards(handcards, remaincards, rank)

    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17, "JOKER": 10000}

    card_value_s2v[rank_card[1]] = 15

    actIndex = 0
    if curAction[0] == "PASS":
        curAction = greaterAction
    print(curAction)
    numofmy = numofplayers[myPos]
    if numofmy <= 10:
        numofnext = numofplayers[(myPos + 1) % 4]
        actIndex = one_hand(numofmy, numofnext, actionList, myPos, greaterPos, 7,
                            restcards, card_value_s2v, rank_card)
        if actIndex != -1:
            return actIndex
    
    if curAction[0] == "Single":

        actIndex = Single(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                               card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "Pair":
        actIndex = Pair(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                             card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "Trips":
        actIndex = Trips(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                              card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "ThreeWithTwo":
        actIndex = ThreeWithTwo(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                                     card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "ThreePair":
        actIndex = ThreePair(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                                  card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "TwoTrips":
        actIndex = TwoTrips(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                                 card_value_s2v, myPos, greaterPos, pass_num, my_pass_num)

    elif curAction[0] == "Straight":
        actIndex = Straight(actionList, curAction, rank_card, handcards, numofplayers, card_value_s2v, pass_num,
                                 my_pass_num, myPos, greaterPos)
    elif curAction[0] == "Bomb" or curAction[0] == "StraightFlush":
        actIndex = Bomb(actionList, curAction, rank_card, handcards, numofplayers, restcards,
                             card_value_s2v, myPos, greaterPos)

    return actIndex
