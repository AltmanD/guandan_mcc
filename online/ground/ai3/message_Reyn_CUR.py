#Reyn_AI 2.0.0 采用加权思想全新改版
#暂定比赛版本
#Author: Ryen Zhang
#University: NUAA

#point-val对应列表
point_val = [28,1,2,3,4,5,7,9,12,15,18,22,25, 100]  # 目前最强版本

#该函数负责转换点数所对应的val
def get_point_val(card,curRank):
    if card[1] == curRank and card[0] == 'H':
        return 500
    if card[1] == curRank:
        return 100
    if card[1] == '2':
        return 1
    if card[1] == '3':
        return 2
    elif card[1] == '4':
        return 3
    elif card[1] == '5':
        return 4
    elif card[1] == '6':
        return 5
    elif card[1] == '7':
        return 6
    elif card[1] == '8':
        return 7
    elif card[1] == '9':
        return 8
    elif card[1] == 'T':
        return 9
    elif card[1] == 'J':
        return 10
    elif card[1] == 'Q':
        return 11
    elif card[1] == 'K':
        return 12
    elif card[1] == 'A':
        return 13
    elif card[1] == 'B':
        return 150
    else:
        return 200

#该函数负责计算剩余的权值
#未考虑三带二之类
def get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank):
    val = 0
    #首先考虑同花顺
    for i in range(9):
        ok = 1
        for j in range(5):
            if handCards_S[i+j] == 0:
                ok = 0
        if ok == 1:
            val += 50 * point_val[i]
            print('Reyn_AI Tip 扫描到同花顺，点数为:',point_val[i])
    for i in range(9):
        ok = 1
        for j in range(5):
            if handCards_H[i+j] == 0:
                ok = 0
        if ok == 1:
            val += 50 * point_val[i]
            print('Reyn_AI Tip 扫描到同花顺，点数为:',point_val[i])
    for i in range(9):
        ok = 1
        for j in range(5):
            if handCards_C[i+j] == 0:
                ok = 0
        if ok == 1:
            val += 50 * point_val[i]
            print('Reyn_AI Tip 扫描到同花顺，点数为:',point_val[i])
    for i in range(9):
        ok = 1
        for j in range(5):
            if handCards_D[i + j] == 0:
                ok = 0
        if ok == 1:
            val += 50 * point_val[i]
            print('Reyn_AI Tip 扫描到同花顺，点数为:',point_val[i])
    #再考虑其他的
    for i in range(13):
        #单张
        if handCards_A[i] == 1:
            val -= 200
            val += point_val[i]
        #对子
        if handCards_A[i] == 2:
            val -= 180
            val += point_val[i] * 2
        #三张
        if handCards_A[i] == 3:
            val -= 300
            val += point_val[i] * 5
        #炸弹
        if handCards_A[i] >= 4:
            val += 100 * point_val[i] * (handCards_A[i] - 3)
    #大小王
    val += handCards_K[0] * 150 + handCards_K[1] * 200
    #级牌
    val += handCards_R[1] * 100 + handCards_R[2] * 500
    return val

#本函数负责计算敌人手牌的价值-没用到
def get_opp_VAL(card,curRank):
    if card[0] == 'Single':
        print('Reyn_AI Tip 确认敌人Action为Single形式')
        val = 0
        val += get_point_val(card[2][0],curRank)
        print('Reyn_AI Tip 敌人的出牌权值为',val)
        return val
    if card[0] == 'Pair':
        print('Reyn_AI Tip 确认敌人Action为Pair形式')
        val = 20
        val += get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        print('Reyn_AI Tip 敌人的出牌权值为',val)
        return val
    if card[0] == 'Trips':
        print('Reyn_AI Tip 确认敌人Action为Trips形式')
        val = 100
        val += get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += 5 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 敌人的出牌权值为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 4:
        print('Reyn_AI Tip 确认敌人Action为Bomb_4形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += 100 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 5:
        print('Reyn_AI Tip 确认敌人Action为Bomb形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += 150 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'Straight':
        print('Reyn_AI Tip 确认敌人Action为Straight形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += 300
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'ThreeWithTwo':
        print('Reyn_AI Tip 确认敌人Action为ThreeWithTwo形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += 200
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'ThreePair':
        print('Reyn_AI Tip 确认敌人Action为ThreePair形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += get_point_val(card[2][5],curRank)
        val += 150
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'TwoTrips':
        print('Reyn_AI Tip 确认敌人Action为TwoTrips形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += get_point_val(card[2][5],curRank)
        val += 120
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    if card[0] == 'StraightFlush':
        print('Reyn_AI Tip 确认敌人Action为StraightFlush形式')
        val = get_point_val(card[2][0],curRank)
        val += get_point_val(card[2][1],curRank)
        val += get_point_val(card[2][2],curRank)
        val += get_point_val(card[2][3],curRank)
        val += get_point_val(card[2][4],curRank)
        val += 180 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 敌人出牌权值为',val)
        return val
    return 3000

#该函数负责获取每步操作的权重，并返回该权重
#接下来会考虑引入递归的方式遍历所有可能情况，做到精准判断权重
#首轮出牌函数
def get_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,card,curRank):
    #计算出的牌减去的权重
    if card[0] == 'PASS':
        return -99999
    if card[0] == 'Single':
        print('Reyn_AI Tip 确认该Action为Single形式')
        val = 100
        val -= get_point_val(card[2][0],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Pair':
        print('Reyn_AI Tip 确认该Action为Pair形式')
        val = 100
        val -= get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        val+=get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Trips':
        print('Reyn_AI Tip 确认该Action为Trips形式')
        val = 80
        val -= get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= 5 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 4:
        print('Reyn_AI Tip 确认该Action为Bomb_4形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= 100 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 5:
        print('Reyn_AI Tip 确认该Action为Bomb形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= 150 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Straight':
        print('Reyn_AI Tip 确认该Action为Straight形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val += 300
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'ThreeWithTwo':
        print('Reyn_AI Tip 确认该Action为ThreeWithTwo形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val += 300
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'ThreePair':
        print('Reyn_AI Tip 确认该Action为ThreePair形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= get_point_val(card[2][5],curRank)
        val += 200
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        if card[2][5] == 'SB':
            handCards_K[0] -= 1
        if card[2][5] == 'HR':
            handCards_K[1] -= 1
        if card[2][5][0] == 'S' and card[2][5][1] != 'B':
            handCards_S[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'H' and card[2][5][1] != 'R':
            handCards_H[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'C':
            handCards_C[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'D':
            handCards_D[get_num(card[2][5][1])] -= 1
        if card[2][5][1] != 'B' and card[2][5][1] != 'R':
            handCards_A[get_num(card[2][5][1])] -= 1
        if card[2][5][1] == curRank:
            handCards_R[1] -= 1
            if card[2][5][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'TwoTrips':
        print('Reyn_AI Tip 确认该Action为TwoTrips形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= get_point_val(card[2][5],curRank)
        val += 200
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        if card[2][5] == 'SB':
            handCards_K[0] -= 1
        if card[2][5] == 'HR':
            handCards_K[1] -= 1
        if card[2][5][0] == 'S' and card[2][5][1] != 'B':
            handCards_S[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'H' and card[2][5][1] != 'R':
            handCards_H[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'C':
            handCards_C[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'D':
            handCards_D[get_num(card[2][5][1])] -= 1
        if card[2][5][1] != 'B' and card[2][5][1] != 'R':
            handCards_A[get_num(card[2][5][1])] -= 1
        if card[2][5][1] == curRank:
            handCards_R[1] -= 1
            if card[2][5][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'StraightFlush':
        print('Reyn_AI Tip 确认该Action为StraightFlush形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= 180 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    return -1500

#接敌人牌函数
def get_VAL_OPP(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,card,curRank):
    #计算出的牌减去的权重
    if card[0] == 'PASS':
        return -99999
    if card[0] == 'Single':
        print('Reyn_AI Tip 确认该Action为Single形式')
        val = -get_point_val(card[2][0],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Pair':
        print('Reyn_AI Tip 确认该Action为Pair形式')
        val =- get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        val+=get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Trips':
        print('Reyn_AI Tip 确认该Action为Trips形式')
        val =- get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= 5 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 4:
        print('Reyn_AI Tip 确认该Action为Bomb_4形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= 100 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Bomb' and len(card[2]) == 5:
        print('Reyn_AI Tip 确认该Action为Bomb形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= 150 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'Straight':
        print('Reyn_AI Tip 确认该Action为Straight形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'ThreeWithTwo':
        print('Reyn_AI Tip 确认该Action为ThreeWithTwo形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'ThreePair':
        print('Reyn_AI Tip 确认该Action为ThreePair形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= get_point_val(card[2][5],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        if card[2][5] == 'SB':
            handCards_K[0] -= 1
        if card[2][5] == 'HR':
            handCards_K[1] -= 1
        if card[2][5][0] == 'S' and card[2][5][1] != 'B':
            handCards_S[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'H' and card[2][5][1] != 'R':
            handCards_H[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'C':
            handCards_C[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'D':
            handCards_D[get_num(card[2][5][1])] -= 1
        if card[2][5][1] != 'B' and card[2][5][1] != 'R':
            handCards_A[get_num(card[2][5][1])] -= 1
        if card[2][5][1] == curRank:
            handCards_R[1] -= 1
            if card[2][5][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'TwoTrips':
        print('Reyn_AI Tip 确认该Action为TwoTrips形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= get_point_val(card[2][5],curRank)
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        if card[2][5] == 'SB':
            handCards_K[0] -= 1
        if card[2][5] == 'HR':
            handCards_K[1] -= 1
        if card[2][5][0] == 'S' and card[2][5][1] != 'B':
            handCards_S[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'H' and card[2][5][1] != 'R':
            handCards_H[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'C':
            handCards_C[get_num(card[2][5][1])] -= 1
        if card[2][5][0] == 'D':
            handCards_D[get_num(card[2][5][1])] -= 1
        if card[2][5][1] != 'B' and card[2][5][1] != 'R':
            handCards_A[get_num(card[2][5][1])] -= 1
        if card[2][5][1] == curRank:
            handCards_R[1] -= 1
            if card[2][5][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    if card[0] == 'StraightFlush':
        print('Reyn_AI Tip 确认该Action为StraightFlush形式')
        val = -get_point_val(card[2][0],curRank)
        val -= get_point_val(card[2][1],curRank)
        val -= get_point_val(card[2][2],curRank)
        val -= get_point_val(card[2][3],curRank)
        val -= get_point_val(card[2][4],curRank)
        val -= 180 * point_val[get_num(card[1])]
        print('Reyn_AI Tip 由于该出牌行动,权值目前为',val)
        #开始删除刚刚打出的牌
        if card[2][0] == 'SB':
            handCards_K[0] -= 1
        if card[2][0] == 'HR':
            handCards_K[1] -= 1
        if card[2][0][0] == 'S' and card[2][0][1] != 'B':
            handCards_S[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'H' and card[2][0][1] != 'R':
            handCards_H[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'C':
            handCards_C[get_num(card[2][0][1])] -= 1
        if card[2][0][0] == 'D':
            handCards_D[get_num(card[2][0][1])] -= 1
        if card[2][0][1] != 'B' and card[2][0][1] != 'R':
            handCards_A[get_num(card[2][0][1])] -= 1
        if card[2][0][1] == curRank:
            handCards_R[1] -= 1
            if card[2][0][0] == 'H':
                handCards_R[2] -= 1
        if card[2][1] == 'SB':
            handCards_K[0] -= 1
        if card[2][1] == 'HR':
            handCards_K[1] -= 1
        if card[2][1][0] == 'S' and card[2][1][1] != 'B':
            handCards_S[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'H' and card[2][1][1] != 'R':
            handCards_H[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'C':
            handCards_C[get_num(card[2][1][1])] -= 1
        if card[2][1][0] == 'D':
            handCards_D[get_num(card[2][1][1])] -= 1
        if card[2][1][1] != 'B' and card[2][1][1] != 'R':
            handCards_A[get_num(card[2][1][1])] -= 1
        if card[2][1][1] == curRank:
            handCards_R[1] -= 1
            if card[2][1][0] == 'H':
                handCards_R[2] -= 1
        if card[2][2] == 'SB':
            handCards_K[0] -= 1
        if card[2][2] == 'HR':
            handCards_K[1] -= 1
        if card[2][2][0] == 'S' and card[2][2][1] != 'B':
            handCards_S[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'H' and card[2][2][1] != 'R':
            handCards_H[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'C':
            handCards_C[get_num(card[2][2][1])] -= 1
        if card[2][2][0] == 'D':
            handCards_D[get_num(card[2][2][1])] -= 1
        if card[2][2][1] != 'B' and card[2][2][1] != 'R':
            handCards_A[get_num(card[2][2][1])] -= 1
        if card[2][2][1] == curRank:
            handCards_R[1] -= 1
            if card[2][2][0] == 'H':
                handCards_R[2] -= 1
        if card[2][3] == 'SB':
            handCards_K[0] -= 1
        if card[2][3] == 'HR':
            handCards_K[1] -= 1
        if card[2][3][0] == 'S' and card[2][3][1] != 'B':
            handCards_S[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'H' and card[2][3][1] != 'R':
            handCards_H[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'C':
            handCards_C[get_num(card[2][3][1])] -= 1
        if card[2][3][0] == 'D':
            handCards_D[get_num(card[2][3][1])] -= 1
        if card[2][3][1] != 'B' and card[2][3][1] != 'R':
            handCards_A[get_num(card[2][3][1])] -= 1
        if card[2][3][1] == curRank:
            handCards_R[1] -= 1
            if card[2][3][0] == 'H':
                handCards_R[2] -= 1
        if card[2][4] == 'SB':
            handCards_K[0] -= 1
        if card[2][4] == 'HR':
            handCards_K[1] -= 1
        if card[2][4][0] == 'S' and card[2][4][1] != 'B':
            handCards_S[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'H' and card[2][4][1] != 'R':
            handCards_H[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'C':
            handCards_C[get_num(card[2][4][1])] -= 1
        if card[2][4][0] == 'D':
            handCards_D[get_num(card[2][4][1])] -= 1
        if card[2][4][1] != 'B' and card[2][4][1] != 'R':
            handCards_A[get_num(card[2][4][1])] -= 1
        if card[2][4][1] == curRank:
            handCards_R[1] -= 1
            if card[2][4][0] == 'H':
                handCards_R[2] -= 1
        val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
        print('Reyn_AI Tip 已计算出该操作权重为',val)
        return val
    return -1500

#将数字与字母兼有的点数转换为纯数字表达形式
#注意，在该AI版本中，所有点数都被转化为了比人类所认为少1的数值，以方便列表的赋值
def get_num(point):
    if point == 'A':
        return 0
    elif point == 'T':
        return 9
    elif point == 'J':
        return 10
    elif point == 'Q':
        return 11
    elif point == 'K':
        return 12
    elif point=='JOKER':
        return 13
    else:
        return int(point) - 1

#判断自己的手牌中是否有接牌的牌型
#'greaterAction': ['Single', '4', ['S4']]
def check_patterns_fri(message,action):
    point_dic={
        '2':0,
        '3':1,
        '4':2,
        '5':3,
        '6':4,
        '7':5,
        '8':6,
        '9':7,
        'T':8,
        'J':9,
        'Q':10,
        'K':11,
        'A':12,
        'B':14,
        'R':15
    }
    action_patterns=action[0]
    action_point=point_dic[action[1]]
    #记录手牌
    handcard_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if message['curRank']==action[1]:
        action_point=13

    for hcard in message['handCards']:
        if hcard[1]==message['curRank']:
            handcard_list[13]+=1
        else:
            handcard_list[point_dic[hcard[1]]]+=1
    #判断牌型是否存在，有则返回1，无则返回0
    #因为有的话却没有打这个牌说明这个牌更重要
    if action_patterns=='Single':
        if handcard_list[action_point]==1:
            return 1
        else:
            return 0

    elif action_patterns=='Pair':
        if handcard_list[action_point]==2:
            return 1
        else:
            return 0
    
    elif action_patterns=='Trips':
        if handcard_list[action_point]==3:
            return 1
        else:
            return 0
    elif action_patterns=='ThreeWithTwo':
        if handcard_list[action_point]==3:
            for point1 in range(0,8):
                if handcard_list[point1]==2:
                    return 1
        else:
            return 0

    elif action_patterns=='ThreePair':
        #因为三联对最大为QQKKAA
        if handcard_list[action_point]==2 and handcard_list[action_point+1]==2 and handcard_list[action_point+2]==2:
            return 1
        else:
            return 0
    #T-J-Q-K-A
    elif action_patterns =='Straight':
        if handcard_list[action_point]==1 and handcard_list[action_point+1]==1 and handcard_list[action_point+2]==1 and handcard_list[action_point+3]==1 and handcard_list[action_point+4]==1 :
            return 1
        else:
            return 0
def check_patterns(message):
     #对照表：
    point_dic={
        '2':0,
        '3':1,
        '4':2,
        '5':3,
        '6':4,
        '7':5,
        '8':6,
        '9':7,
        'T':8,
        'J':9,
        'Q':10,
        'K':11,
        'A':12,
        'B':14,
        'R':15
    }
    action_patterns=message['greaterAction'][0]
    #记录手牌
    handcard_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if message['curRank']==message['greaterAction'][1]:
        action_point=13
    elif message['greaterAction'][1]=='JOKER':
        return 1
    else:
        action_point=point_dic[message['greaterAction'][1]]

    for hcard in message['handCards']:
        if hcard[1]==message['greaterAction'][1]:
            handcard_list[13]+=1
        else:
            handcard_list[point_dic[hcard[1]]]+=1
    #判断牌型是否存在，有则返回1，无则返回0
    #因为有的话却没有打这个牌说明这个牌更重要
    if action_patterns=='Single':
        if action_point==15:
            return 0
        for point in range(action_point+1,16):
            if handcard_list[point]==1:
                return 1
        else:
            return 0

    elif action_patterns=='Pair':
        if action_point==15:
            return 0
        for point in range(action_point+1,16):
            if handcard_list[point]==2:
                return 1
        else:
            return 0
    
    elif action_patterns=='Trips':
        if action_point==15:
            return 0
        for point in range(action_point+1,16):
            if handcard_list[point]==3:
                return 1
        else:
            return 0
    elif action_patterns=='ThreeWithTwo':
        for point in range(action_point+1,16):
            if handcard_list[point]==3:
                for point1 in range(0,12):
                    if handcard_list[point1]==2:
                        return 1
        else:
            return 0

    elif action_patterns=='ThreePair':
        #因为三联对最大为QQKKAA
        if action_point>=10:
            return 0
        for point in range(action_point+1,11):
            if handcard_list[point]==2 and handcard_list[point+1]==2 and handcard_list[point+2]==2:
                return 1
        else:
            return 0
    #T-J-Q-K-A
    elif action_patterns =='Straight':
        for point in range(action_point+1,9):
            if handcard_list[point]==1 and handcard_list[point+1]==1 and handcard_list[point+2]==1 and handcard_list[point+3]==1 and handcard_list[point+4]==1 :
                return 1
        else:
            return 0
            

        
def check_message(message,pos):
    #读取当前牌局的等级 
    curRank = message['curRank']
    print('Reyn_AI Tip 已读取到当前等级为:',curRank)
    
    #还贡判断
    if message['stage'] == 'back':
        #开始遍历Actionlist
        index = -1
        #创建空操作权重列表[权重值]
        value = []
        for check_card in message['actionList']:
            index += 1
            print('Reyn_AI Tip 当前判断Action',index,':',check_card)
            #读取手牌部分开始
            print('Reyn_AI Log 进入到读取手牌部分')
            #创建按花色和顺序归类好的牌库，数值为该牌拥有的数量
            #黑桃:S 红桃:H 梅花:C 方片:D
            #花色牌列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_S = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_H = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_C = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_D = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #数值总列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_A = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #级牌列表[点数-级牌数量-红桃级牌数量]
            handCards_R = [get_num(curRank)+1,0,0]
            #特殊牌列表[数量] 序号-点数 分别为:[0-B,1-R]
            handCards_K = [0,0]
            #遍历服务器所给的'handCards'，为上述数据赋值
            for card in message['handCards']:
                if card[1] == curRank:
                    handCards_R[1] += 1
                    if card[0] == 'H':
                        handCards_R[2] += 1

                if card[1] == 'B' or card[1] == 'R':
                    if card[1] == 'B':
                        handCards_K[0] += 1
                    if card[1] == 'R':
                        handCards_K[1] += 1
                else:
                    if card[0] == 'S' and card[1] != 'B':
                        handCards_S[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'H' and card[1] != 'R':
                        handCards_H[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'C':
                        handCards_C[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'D':
                        handCards_D[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
            #print('Reyn_AI Log 读取手牌部分结束')
            #print('Reyn_AI Tip 当前读取到的手牌为')
            #print('handCards_S:',handCards_S)
            #print('handCards_H:',handCards_H)
            #print('handCards_C:',handCards_C)
            #print('handCards_D:',handCards_D)
            #print('handCards_A:',handCards_A)
            #print('handCards_R:',handCards_R)
            #print('handCards_K:',handCards_K)
            #读取手牌部分结束
            print('Reyn_AI Tip 开始选择最优还贡牌')
            val = -get_point_val(check_card[2][0],curRank)
            print('Reyn_AI Tip 由于该还贡行动,权值目前为',val)
            #开始删除刚刚打出的牌
            if check_card[2][0] == 'SB':
                handCards_K[0] -= 1
            if check_card[2][0] == 'HR':
                handCards_K[1] -= 1
            if check_card[2][0][0] == 'S' and check_card[2][0][1] != 'B':
                handCards_S[get_num(check_card[2][0][1])] -= 1
            if check_card[2][0][0] == 'H' and check_card[2][0][1] != 'R':
                handCards_H[get_num(check_card[2][0][1])] -= 1
            if check_card[2][0][0] == 'C':
                handCards_C[get_num(check_card[2][0][1])] -= 1
            if check_card[2][0][0] == 'D':
                handCards_D[get_num(check_card[2][0][1])] -= 1
            if check_card[2][0][1] != 'B' and check_card[2][0][1] != 'R':
                handCards_A[get_num(check_card[2][0][1])] -= 1
            if check_card[2][0][1] == curRank:
                handCards_R[1] -= 1
                if check_card[2][0][0] == 'H':
                    handCards_R[2] -= 1
            val += get_remain_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,curRank)
            print('Reyn_AI Tip 已计算出该操作权重为',val)
            value.append(val)
        max = -50000
        AI_choice = 0
        for i in range(index + 1):
            if value[i] > max:
                AI_choice = i
                max = value[i]
        print(value)
        return AI_choice

    #我方先手 AI选择部分开始
    if message['greaterPos']==pos or message['greaterPos']==-1:
        print('Reyn_AI Tip 轮到我方先手出牌')
        #开始遍历Actionlist
        index = -1
        #创建空操作权重列表[权重值]
        value = []
        for check_card in message['actionList']:
            index += 1
            print('Reyn_AI Tip 当前判断Action',index,':',check_card)
            #读取手牌部分开始
            print('Reyn_AI Log 进入到读取手牌部分')
            #创建按花色和顺序归类好的牌库，数值为该牌拥有的数量
            #黑桃:S 红桃:H 梅花:C 方片:D
            #花色牌列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_S = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_H = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_C = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_D = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #数值总列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_A = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #级牌列表[点数-级牌数量-红桃级牌数量]
            handCards_R = [get_num(curRank)+1,0,0]
            #特殊牌列表[数量] 序号-点数 分别为:[0-B,1-R]
            handCards_K = [0,0]
            #遍历服务器所给的'handCards'，为上述数据赋值
            for card in message['handCards']:
                if card[1] == curRank:
                    handCards_R[1] += 1
                    if card[0] == 'H':
                        handCards_R[2] += 1

                if card[1] == 'B' or card[1] == 'R':
                    if card[1] == 'B':
                        handCards_K[0] += 1
                    if card[1] == 'R':
                        handCards_K[1] += 1
                else:
                    if card[0] == 'S' and card[1] != 'B':
                        handCards_S[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'H' and card[1] != 'R':
                        handCards_H[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'C':
                        handCards_C[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'D':
                        handCards_D[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
            #print('Reyn_AI Log 读取手牌部分结束')
            #print('Reyn_AI Tip 当前读取到的手牌为')
            #print('handCards_S:',handCards_S)
            #print('handCards_H:',handCards_H)
            #print('handCards_C:',handCards_C)
            #print('handCards_D:',handCards_D)
            #print('handCards_A:',handCards_A)
            #print('handCards_R:',handCards_R)
            #print('handCards_K:',handCards_K)
            #读取手牌部分结束
            value.append(get_VAL(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,check_card,curRank))
        max = -50000
        AI_choice = 0
        for i in range(index + 1):
            if value[i] > max:
                AI_choice = i
                max = value[i]
        print(value)
        return AI_choice
    
    #接队友牌
        #对照表：
    point_dic={
        'A':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'T':10,
        'J':11,
        'Q':12,
        'K':13,
        'B':14,
        'R':15
    }
    if message['greaterPos']==(pos+2)%4:
        own_side_action=message['greaterAction'][0]
        own_side_point=message['greaterAction'][1]
        if own_side_action=='Bomb':
            return 0
        elif own_side_action=='Single' or own_side_action=='Pair' or own_side_action=='Trips' or own_side_action=='ThreeWithTwo':
            if own_side_point=='T' or own_side_point=='J' or own_side_point=='Q' or own_side_point=='K'  or own_side_point=='A' or own_side_point=='B' or own_side_point=='R' or own_side_point==message['curRank']:
                return 0
        elif own_side_action=='ThreePair' or own_side_action=='TripsPair':
            if own_side_point=='T' or own_side_point=='J' or own_side_point=='Q' or own_side_point=='K' or own_side_point=='A':
                return 0
        elif own_side_action=='Straight':
            if own_side_point=='7' or own_side_point=='8' or own_side_point=='9' or own_side_point=='T' or own_side_point=='J':
                return 0
        elif own_side_action=='StraightFlush':
            return 0
        elif own_side_action=='JOKER':
            return 0
        # 对选择完的牌型做进一步缩小范围
        index=-1
        #创建按花色和顺序归类好的牌库，数值为该牌拥有的数量
        #黑桃:S 红桃:H 梅花:C 方片:D
        #花色牌列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
        handCards_S = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        handCards_H = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        handCards_C = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        handCards_D = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        #数值总列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
        handCards_A = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        #级牌列表[点数-级牌数量-红桃级牌数量]
        handCards_R = [get_num(curRank)+1,0,0]
        #特殊牌列表[数量] 序号-点数 分别为:[0-B,1-R]
        handCards_K = [0,0]
        for check_card in message['actionList']:
            index += 1
            print('Reyn_AI Tip 当前判断Action',index,':',check_card)
            #读取手牌部分开始
            print('Reyn_AI Log 进入到读取手牌部分')
            
            #遍历服务器所给的'handCards'，为上述数据赋值
            for card in message['handCards']:
                if card[1] == curRank:
                    handCards_R[1] += 1
                    if card[0] == 'H':
                        handCards_R[2] += 1

                if card[1] == 'B' or card[1] == 'R':
                    if card[1] == 'B':
                        handCards_K[0] += 1
                    if card[1] == 'R':
                        handCards_K[1] += 1
                else:
                    if card[0] == 'S' and card[1] != 'B':
                        handCards_S[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'H' and card[1] != 'R':
                        handCards_H[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'C':
                        handCards_C[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'D':
                        handCards_D[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
        val=[]
        action_List=message['actionList']
        for action_index in range(len(action_List)):
            if 'H'+message['curRank'] in action_List[action_index][2]:
                val.append(-100000)
                continue
            if action_List[action_index][0]==own_side_action and action_List[action_index][1] != message['curRank']:
                if point_dic[action_List[action_index][1]]-point_dic[own_side_point]<=2 and check_patterns_fri(message,action_List[action_index]):
                    val.append(get_VAL_OPP(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,action_List[action_index],curRank))
                else:
                    val.append(-100000)
            else:
                val.append(-100000)
        max = -50000
        AI_choice = 0
        for i in range(index + 1):
            if val[i] > max:
                AI_choice = i
                max = val[i]
        print(val)
        return AI_choice

    else:
        print('Reyn_AI Tip 轮到我方迎接敌人')
        check_pass=True
        #if not check_patterns(message) and message['publicInfo'][int(message['greaterPos'])]['rest']>=17:
            # opp_side_action=message['greaterAction'][0]
            # opp_side_point=message['greaterAction'][1]
            # if opp_side_action=='Single' or opp_side_action=='Pair' or opp_side_action=='Trips' :
            #     if opp_side_point=='B' or opp_side_point=='R' or opp_side_point==message['curRank']:
            #         check_pass=False
            #     if check_pass:
            #         return 0
            # elif opp_side_action=='ThreePair' or opp_side_action=='TripsPair' or opp_side_action=='ThreeWithTwo':
            #     if opp_side_point=='T' or opp_side_point=='J' or opp_side_point=='Q' or opp_side_point=='K' or opp_side_point=='A':
            #         check_pass=False
            #     if check_pass:
            #         return 0
        
        #    return 0

        #开始遍历Actionlist
        index = -1
        #创建空操作权重列表[权重值]
        value = []
        for check_card in message['actionList']:
            index += 1
            print('Reyn_AI Tip 当前判断Action',index,':',check_card)
            #读取手牌部分开始
            print('Reyn_AI Log 进入到读取手牌部分')
            #创建按花色和顺序归类好的牌库，数值为该牌拥有的数量
            #黑桃:S 红桃:H 梅花:C 方片:D
            #花色牌列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_S = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_H = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_C = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            handCards_D = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #数值总列表[数量] 序号-点数 分别为:[0-A,1-2,2-3,3-4,4-5,5-6,6-7,7-8,8-9,9-T,10-J,11-Q,12-K]
            handCards_A = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #级牌列表[点数-级牌数量-红桃级牌数量]
            handCards_R = [get_num(curRank)+1,0,0]
            #特殊牌列表[数量] 序号-点数 分别为:[0-B,1-R]
            handCards_K = [0,0]
            #遍历服务器所给的'handCards'，为上述数据赋值
            for card in message['handCards']:
                if card[1] == curRank:
                    handCards_R[1] += 1
                    if card[0] == 'H':
                        handCards_R[2] += 1

                if card[1] == 'B' or card[1] == 'R':
                    if card[1] == 'B':
                        handCards_K[0] += 1
                    if card[1] == 'R':
                        handCards_K[1] += 1
                else:
                    if card[0] == 'S' and card[1] != 'B':
                        handCards_S[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'H' and card[1] != 'R':
                        handCards_H[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'C':
                        handCards_C[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
                    if card[0] == 'D':
                        handCards_D[get_num(card[1])] += 1
                        handCards_A[get_num(card[1])] += 1
            #print('Reyn_AI Log 读取手牌部分结束')
            #print('Reyn_AI Tip 当前读取到的手牌为')
            #print('handCards_S:',handCards_S)
            #print('handCards_H:',handCards_H)
            #print('handCards_C:',handCards_C)
            #print('handCards_D:',handCards_D)
            #print('handCards_A:',handCards_A)
            #print('handCards_R:',handCards_R)
            #print('handCards_K:',handCards_K)
            #读取手牌部分结束
            #开始计算地方卡牌权值
            card_opp = message['greaterAction']
            value.append(get_VAL_OPP(handCards_S,handCards_H,handCards_C,handCards_D,handCards_A,handCards_R,handCards_K,check_card,curRank))
        # if message['publicInfo'][(pos+3)%4]['rest']>=15 or message['publicInfo'][(pos+1)%4]['rest']>=15:
        #     if message['greaterAction'][0]!='Straight' and message['greaterAction'][0]!='StraightFlush' and message['greaterAction'][0]!='Bomb':
        #         for i in range(len(message['actionList'])):
        #             if message['actionList'][i][0]=='Bomb' or message['actionList'][i][0]=='StraightFlush':
        #                 value[i]=-200000
        max = -50000
        AI_choice = 0
        for i in range(index + 1):
            if value[i] > max:
                AI_choice = i
                max = value[i]
        print(value)
        return AI_choice

          