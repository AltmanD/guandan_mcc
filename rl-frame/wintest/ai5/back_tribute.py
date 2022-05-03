#!/usr/bin/env python
# encoding: utf-8
"""
@author:Naynix
@contact: naynix@qq.com
@file: back.py.py
@time: 2020/10/26 20:54
"""
from random import randint

from utils.utils import combine_handcards


def back_action(msg, mypos, tribute_result):
    rank = msg["curRank"]
    action = msg["actionList"]
    handCards = msg["handCards"]
    card_val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_val[rank] = 15

    def flag_TJQ(handCards_X) -> tuple:
        # 传入的参数为combined_handcards["X"]，判断combined_handcards["X"]中是否有TJQ
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
        # 获取card（例如'D3'）在actionList中的index
        for i in range(len(action)):
            if action[i][2][0] == target:
                return i

    def choose_in_single(single_list) -> str:
        # 根据单张还贡
        # 进贡结果 0向3进贡 "result": [[0, 3, 'S2']] 或 [[0, 3, 'S2'], [2, 1, 'S2']]
        for my_pos in tribute_result:
            if my_pos[1] == mypos:
                tribute_pos = my_pos[0]

        n = len(single_list)
        if (int(tribute_pos) + int(mypos)) % 2 != 0:  # 给对手还贡
            for card in single_list:
                if card in ['H5', 'HT']:  # 优先还H5，HT
                    return card
                elif card in ['S5', 'C5', 'D5', 'ST', 'CT', 'DT']:
                    return card  # 其次还其他花色的5或10
            # 以上均没有，则随机还
            return single_list[randint(0, n - 1)]
        else:  # 给对家还贡，优先还小于5的单张
            back_list = []
            for card in single_list:
                if card[-1] != 'T':
                    if int(card[-1]) < 5:
                        back_list.append(card)  # 将小于5的单张加入到back_list中
            if back_list:
                return back_list[randint(0, len(back_list) - 1)]
            return single_list[randint(0, n - 1)]

    def choose_in_pair(pair_list, pair_list_from_handcards) -> str:
        # 根据对子还贡，还最小的未组成连对的牌
        val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
        if len(pair_list) < 3:
            return pair_list[0][0]
        for i in range(len(pair_list)):
            flag = False
            if i >= 2:
                # 检查前项
                pair_first_val, pair_second_val, pair_third_val = pair_list[i - 2][0][-1], pair_list[i - 1][0][-1], \
                                                                  pair_list[i][0][-1]
                if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                        val_dict[pair_third_val] - 1:
                    flag = True
            if 1 <= i <= len(pair_list) - 2:
                # 检查中项
                pair_first_val, pair_second_val, pair_third_val = pair_list[i - 1][0][-1], pair_list[i][0][-1], \
                                                                  pair_list[i + 1][0][-1]
                if val_dict[pair_first_val] == val_dict[pair_second_val] - 1 and val_dict[pair_second_val] == \
                        val_dict[pair_third_val] - 1:
                    flag = True
            if i <= len(pair_list) - 3:
                # 检查后项
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
        return pair_list[0][0]  # 均可组成连对，则还最小的一张

    def choose_in_trips(trips_list, trips_list_from_handcards) -> str:
        # 根据三张还贡，还最小的未组成钢板的牌
        val_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10}
        if len(trips_list) < 2:
            return trips_list[0][0]
        for i in range(len(trips_list)):
            flag = False
            if i >= 1:
                # 检查前项
                pair_first_val, pair_second_val = trips_list[i - 1][0][-1], trips_list[i][0][-1]
                if val_dict[pair_first_val] == val_dict[pair_second_val] - 1:
                    flag = True
            if i <= len(trips_list) - 2:
                # 检查后项
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
        return trips_list[0][0]  # 均可组成三张，则还最小的一张

    def choose_in_bomb(bomb_list, bomb_info) -> str:
        # 根据炸弹还贡

        def get_card_from_bomb(bomb_list, key):
            # 根据key从炸弹牌中取一张
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
        # 有单张时
        card = choose_in_single(combined_temp["Single"])
    elif combined_temp["Trips"]:
        # 没有单张，但有三张时
        card = choose_in_trips(combined_temp["Trips"], combined_handcards["Trips"])
    elif combined_temp["Pair"]:
        # 没有单张、三张，但有对子时
        card = choose_in_pair(combined_temp["Pair"], combined_handcards["Pair"])
    elif combined_temp["Bomb"]:
        # 没有单张、对子、三张，但有炸弹时
        card = choose_in_bomb(combined_temp["Bomb"], temp_bomb_info)
    else:
        # 其他情况随机
        temp = []  # 可还的牌
        for handCard in handCards:
            if card_val[handCard[-1]] <= 10:
                temp.append(handCard)
        card = temp[randint(0, len(temp) - 1)]
    return get_card_index(card)

def tribute(actionList,rank):

    rank_card = 'H'+rank
    first_action = actionList[0]
    if rank_card in first_action[2]:
        return 1
    else:
        return 0
