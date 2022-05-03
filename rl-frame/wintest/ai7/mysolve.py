# -*- coding: utf-8 -*-
# @Time       : 2020/10/19 19:30
# @Author     : Zenghui Qian
# @File       : mysolve.py
# @Description: 开门见山得说，我们的算法几乎与人工智能不沾边，仅仅是人工设置的评估函数（不知道会不会被退赛 -_-||）。
# 这个评估函数大致是这样的形式：
# Score = Gain * ( 1 + Possibility ) / Value;（算法会优先打出评分较高的打法）
# 因此，我们算法的上限并不会超过人的思维层面，换句话说，就是顶多模拟出一个记牌能力极强并且有固定出牌策略（人为设定）的牌手。
# 所以，这个算法唯一可能的前途就是充当训练AI模型的数据来源。应该会比“笨笨”提供的数据更有效，更有针对性（至少我是这么想的）。
# 现阶段算法的模拟效果：已经能根据具体情况做出一些看起来“智能”的决策，能够比较轻松地战胜一些未成熟的算法（至少目前是）。
# 时间充足的话，会努力自学，写出AI算法，谢谢(*°∀°)=3


#              0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
str_to_ind = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'L', 'B', 'R']
#              0    1    2    3
str_to_flo = ['S', 'H', 'C', 'D']


def card_to_list(card, my_list, step):
    des = str_to_flo.index(card[0])
    #  数字
    if card[1] == 'T':
        my_list[des][8] += step
        my_list[4][8] += step
    elif card[1] == 'J':
        my_list[des][9] += step
        my_list[4][9] += step
    elif card[1] == 'Q':
        my_list[des][10] += step
        my_list[4][10] += step
    elif card[1] == 'K':
        my_list[des][11] += step
        my_list[4][11] += step
    elif card[1] == 'A':
        my_list[des][12] += step
        my_list[4][12] += step
    elif card[1] == 'B':
        my_list[des][13] += step
    elif card[1] == 'R':
        my_list[des][13] += step
    else:
        my_list[des][int(card[1]) - 2] += step
        my_list[4][int(card[1]) - 2] += step


def getval(card, rank, has):               # 评估一张牌在手牌中的价值，card: 牌面 如"H2"，rank 当前等级，has 手牌情况
    des = str_to_flo.index(card[0])
    val = str_to_ind.index(card[1]) + 1
    index = str_to_ind.index(card[1])
    if card[1] == 'B' or card[1] == 'R':
        index = 13
    if card[1] == rank:                     # 对级牌重新赋予价值
        val = 14
    if card == 'SB':                        # 对大王小王重新赋予价值
        if has[0][13] == 2 and has[1][13] == 2:
            val *= 100
        elif has[0][13] == 2 and has[1][13] != 2:
            val += 20
    elif card == 'HR':
        if has[0][13] == 2 and has[1][13] == 2:
            val *= 100
        elif has[0][13] != 2 and has[1][13] == 2:
            val += 20
    elif card[0] == 'H' and card[1] == rank:    # 对红桃级牌重新赋予价值
        val = 340
    else:
        ans = 0                         # ans 暂时记录构成同花顺的牌的新价值
        for num in range(index-4, index+1):   # 搜寻同花顺
            if num >= -1 and num+4 <= 12:
                if num == -1:
                    if has[des][12] >= 1 and has[des][0] >= 1 and has[des][1] >= 1 and has[des][2] >= 1 \
                            and has[des][3] >= 1:
                        ans = 320+val
                else:
                    if has[des][num] >= 1 and has[des][num+1] >= 1 and has[des][num+2] >= 1 and has[des][num+3] >= 1 \
                            and has[des][num+4] >= 1:
                        ans = 320+val
        if has[4][index] <= 3:          # 查看同点数的牌的数目，根据数目重新赋予价值
            val += 20 * (has[4][index]-1)
        elif has[4][index] == 4:
            val += 220
        elif has[4][index] == 5:
            val += 300
        elif has[4][index] == 6:        # 修改了超过5张的赋值，是更符合出牌逻辑 2020.10.21
            val += 400                  # 再次修改  2020.10.23
        elif has[4][index] == 7:
            val += 500
        elif has[4][index] == 8:
            val += 600
        if val < ans:                   # 取val 和 ans 中较大者为最终价值
            val = ans
    return val                          # 评估完成，返回该牌的价值


def cac(gain, value, poss):             # 评分计算公式 有待完善
    return gain*(1 + poss)/value        # Score = Gain * ( 1 + Possibility ) / Value;（算法会优先打出评分较高的打法）


def solve(msg, mate_pos):                   # 主体函数  生成记录手牌情况的列表
    zero_s_cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]       # 2 -- 王
    zero_h_cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zero_c_cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]          # 2 -- A
    zero_d_cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zero_number_cards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]     # 2 -- A
    zero_rank_cards = [0, 0]            # 非红桃 红桃

    has = [zero_s_cards, zero_h_cards, zero_c_cards, zero_d_cards, zero_number_cards, zero_rank_cards]
    now_rank = msg["curRank"]           # 获取等级
    now_greater_pos = msg["greaterPos"]
    op1_pos = (mate_pos + 1) % 4
    op2_pos = (mate_pos + 3) % 4

    for card in msg["handCards"]:       # 统计当前手牌
        if card[1] == now_rank and card[0] == 'H':
            has[5][1] += 1
        elif card[1] == now_rank and card[0] != 'H':
            has[5][0] += 1
        card_to_list(card, has, 1)

    act_score = []                  # 存放所有行动选项的评分

    for action in msg["actionList"]:   # 对所有行动选项进行评估
        if len(action[2]) == len(msg["handCards"]):
            act_score.append(100000)
        else:
            if action[0] == "Single":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(1, value, poss)
                n_score = score
                if now_greater_pos == -1:
                    if msg["publicInfo"][op1_pos]['rest'] == 1:
                        n_score = -1 * score
                    if msg["publicInfo"][mate_pos]['rest'] == 1:
                        n_score = score + 100
                    if msg["publicInfo"][op2_pos]['rest'] == 1:
                        n_score = -1 * score
                    act_score.append(n_score)
                else:
                    if msg["publicInfo"][op1_pos]['rest'] == 1:
                        n_score = score
                    if msg["publicInfo"][mate_pos]['rest'] == 1:
                        n_score = -10000
                    if msg["publicInfo"][op2_pos]['rest'] == 1:
                        n_score = -1 * score
                    act_score.append(n_score)

            elif action[0] == "Pair":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(2, value, poss)
                n_score = score
                if now_greater_pos == -1:
                    if msg["publicInfo"][op1_pos]['rest'] == 2:
                        n_score = -1 * score
                    if msg["publicInfo"][mate_pos]['rest'] == 2:
                        n_score = score + 100
                    if msg["publicInfo"][op2_pos]['rest'] == 2:
                        n_score = -1 * score
                    act_score.append(n_score)
                else:
                    if msg["publicInfo"][op2_pos]['rest'] == 2 or msg["publicInfo"][op2_pos]['rest'] == 2:
                        n_score = -1 * score
                    act_score.append(n_score)

            elif action[0] == "Trips":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(3, value, poss)
                n_score = score
                if now_greater_pos == -1:
                    if msg["publicInfo"][op1_pos]['rest'] == 3:
                        n_score = -1 * score
                    if msg["publicInfo"][op2_pos]['rest'] == 3:
                        n_score = -1 * score
                    act_score.append(n_score)
                else:
                    if msg["publicInfo"][op1_pos]['rest'] == 3 or msg["publicInfo"][op2_pos]['rest'] == 3:
                        n_score = -1 * score
                    act_score.append(n_score)

            elif action[0] == "ThreePair":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(6, value, poss)
                act_score.append(score)

            elif action[0] == "ThreeWithTwo":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = (max(values) + min(values)) / 2
                poss = 1
                score = cac(5, value, poss)
                act_score.append(score)

            elif action[0] == "TwoTrips":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(6, value, poss)
                act_score.append(score)

            elif action[0] == "Straight":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = sum(values)
                poss = 1
                score = cac(5, value, poss)
                act_score.append(score)

            elif action[0] == "StraightFlush":
                if now_greater_pos == mate_pos or now_greater_pos == -1:
                    act_score.append(-10000)    # 如果是队友，就不会出同花顺  解决 接队友单张时不能排除的问题  2020.10.20
                elif now_greater_pos == op1_pos or now_greater_pos == op2_pos:
                    if msg["publicInfo"][now_greater_pos]['rest'] <= 14:
                        values = []
                        for one in action[2]:
                            values.append(getval(one, now_rank, has))
                        value = max(values)
                        poss = 1
                        score = cac(5, value, poss)
                        act_score.append(score)
                    else:
                        act_score.append(-1)

            elif action[0] == "Bomb":
                if now_greater_pos == mate_pos or now_greater_pos == -1:
                    act_score.append(-10000)    # 如果是队友，就不会出炸弹    解决 接队友单张时不能排除的问题  2020.10.20
                elif now_greater_pos == op1_pos or now_greater_pos == op2_pos:
                    if msg["publicInfo"][now_greater_pos]['rest'] <= 14:
                        values = []
                        for one in action[2]:
                            values.append(getval(one, now_rank, has))
                        value = max(values)
                        poss = 1
                        score = cac(len(values), value, poss)
                        act_score.append(score)
                    else:
                        act_score.append(-1)

            elif action[0] == "PASS":
                if now_greater_pos == mate_pos:
                    if msg["publicInfo"][mate_pos]['rest'] <= 6:  # 队友的牌数小于6时，不会压队友  PASS优先级最高
                        value = 1
                        poss = 1
                        score = cac(1, value, poss)
                        act_score.append(score)
                    else:
                        if msg["greaterAction"][0] == "Single":  # 单张情况  酌情设置PASS优先级
                            value = 25
                            poss = 1
                            score = cac(2, value, poss)
                            act_score.append(score)
                        elif msg["greaterAction"][0] == "Pair":  # 对子情况  酌情设置PASS优先级
                            value = 65
                            poss = 1
                            score = cac(4, value, poss)
                            act_score.append(score)
                        elif msg["greaterAction"][0] == "Trips":  # 对子情况  酌情设置PASS优先级
                            value = 103
                            poss = 1
                            score = cac(6, value, poss)
                            act_score.append(score)
                        else:                               # 不会压队友  PASS优先级最高
                            value = 1
                            poss = 1
                            score = cac(1, value, poss)
                            act_score.append(score)
                else:                                       # 对方牌权  PASS优先级最低
                    if 1 <= msg["publicInfo"][op2_pos]['rest'] <= 3 :
                        act_score.append(-9999)
                    else:
                        value = 1
                        poss = 1
                        score = cac(0, value, poss)
                        act_score.append(score)

            elif action[0] == "back":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(1, value, poss)
                act_score.append(score)

            elif action[0] == "tribute":
                values = []
                for one in action[2]:
                    values.append(getval(one, now_rank, has))
                value = max(values)
                poss = 1
                score = cac(1, value, poss)
                act_score.append(score)

    return act_score.index(max(act_score))     # 返回所有选项中分数最高的选项的下标
