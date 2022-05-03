#!/usr/bin/env python
# encoding: utf-8
"""
@author:Naynix
@contact: naynix@qq.com
@file: active.py
@time: 2020/10/26 21:08
"""
from utils.utils import *


def getlist( handcards, rank):
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
    sorted_cards, bomb_info = combine_handcards(handcards, rank, card_value_s2v)

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

    return sorted_cards, single_actionlist, pair_actionlist, trips_actionlist, threepair_actionlist, threetwo_actionlist, twotrips_actionlist, straight_actionlist


def active( actionList, handcards, rank, numofplayers, mypos, remaincards):
    restcards = rest_cards(handcards, remaincards, rank)
    rank_card = 'H' + rank
    numofnext = numofplayers[(mypos + 1) % 4]
    if numofnext == 0:
        numofnext = numofplayers[(mypos - 1) % 4]

    cur = [9, 10, 9, 8, 10, 10, 2]
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v2 = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13, "B": 16, "R": 17}
    card_value_s2v[rank] = 15

    sorted_cards, single_actionlist, pair_actionlist, trips_actionlist, threepair_actionlist, threetwo_actionlist, twotrips_actionlist, straight_actionlist = self.getlist(
        handcards, rank)
    print(len(single_actionlist), len(pair_actionlist), len(trips_actionlist), len(threetwo_actionlist),
          len(threepair_actionlist), len(twotrips_actionlist), len(straight_actionlist))

    max_val = card_value_s2v[restcards[-1][0][-1]]

    for i in actionList:
        if len(handcards) == len(i[2]):
            return actionList.index(i)

    twohand_candidatelist = []

    def mysort2(elem):
        return elem[1]

    if len(handcards) <= 12:
        for i in range(len(actionList)):
            for j in range(i + 1, len(actionList)):
                if len(actionList[i][-1]) + len(actionList[j][-1]) == len(handcards):
                    combine_list = actionList[i][-1] + actionList[j][-1]
                    if combine_list.sort(key=mysort2) == handcards.sort(key=mysort2):
                        twohand_candidatelist.append((i, j))

    if len(single_actionlist) and card_value_s2v[single_actionlist[0][0]] < cur[0]:
        if numofnext == 1:
            pass
        else:
            return getindex("Single", single_actionlist, actionList)

    if len(threepair_actionlist) or len(twotrips_actionlist):
        index = rankfour(twotrips_actionlist, threepair_actionlist, actionList, cur[1], cur[2])
        if index is None:
            pass
        else:
            return index

    if len(straight_actionlist) and card_value_s2v2[straight_actionlist[0][0]] < cur[4]:
        return getindex("Straight", straight_actionlist, actionList)

    if len(threetwo_actionlist):

        index = rankthree(single_actionlist, pair_actionlist, trips_actionlist, threetwo_actionlist, actionList,
                          numofnext,
                          rank, cur[0], cur[3], cur[4], cur[5], cur[-1])
        if index is None:
            pass
        else:
            return index
    if len(trips_actionlist):
        return rankone(single_actionlist, trips_actionlist, actionList, numofnext, rank)
    if len(pair_actionlist):
        return ranktwo(handcards, single_actionlist, pair_actionlist, trips_actionlist, actionList, numofnext, rank,
                       max_val)
    if len(single_actionlist):
        if numofnext == 1 and len(trips_actionlist) == 0 and len(pair_actionlist) == 0 and rank_card in handcards:
            for i in range(len(actionList)):
                if actionList[i][0] == 'Pair' and (
                        actionList[i][-1][0] in sorted_cards['Single'] or actionList[i][-1][-1] in sorted_cards['Single']):
                    return i
        if numofnext == 1:
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
        return 0
