import copy

def combine_handcards(handcards, rank, card_val):
    cards = {}
    cards["Single"] = []
    cards["Pair"] = []
    cards["Trips"] = []
    cards["Bomb"] = []
    bomb_info = {}

    handcards = sorted(handcards, key=lambda item: card_val[item[1]])
    start = 0
    for i in range(1, len(handcards) + 1):
        if i == len(handcards) or handcards[i][-1] != handcards[i - 1][-1]:
            if (i - start == 1):
                cards["Single"].append(handcards[i - 1])
            elif (i - start == 2):
                cards["Pair"].append(handcards[start:i])
            elif (i - start) == 3:
                cards["Trips"].append(handcards[start:i])
            else:
                cards["Bomb"].append(handcards[start:i])
                bomb_info[handcards[start][-1]] = i - start
            start = i

    rank = rank
    temp = []
    for i in handcards:
        if i[-1] != rank and i[-1] != 'B' and i[-1] != 'R':
            temp.append(i)
    for i in cards['Bomb']:
        if i[0][-1] != rank and i[0][-1] != 'B' and i[0][-1] != 'R':
            for j in i:
                temp.remove(j)
    cardre = [0] * 14
    cardre_value_s2v = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13}
    for i in temp:
        cardre[cardre_value_s2v[i[-1]]] +=1
    st = []
    minnum = 10
    mintwonum = 10

    for i in range(1, len(cardre) - 4):
        if 0 not in cardre[i:i + 5]:
            onenum = 0
            zeronum = 0
            twonum = 0
            for j in cardre[i:i + 5]:
                if j - 1 == 0:
                    zeronum += 1
                if j - 1 == 1:
                    onenum += 1
                if j - 1 == 2:
                    twonum += 1

            if zeronum > onenum and minnum >= onenum:
                if len(st) == 0:
                    if zeronum >= onenum + twonum:
                        st.append(i)
                        minnum = onenum
                        mintwonum = twonum
                else:
                    if minnum == onenum:
                        if i == 1:
                            if mintwonum > twonum:
                                if zeronum >= onenum + twonum:
                                    st = []
                                    st.append(i)
                                    minnum = onenum
                                    mintwonum = twonum
                        else:
                            if mintwonum >= twonum:
                                if zeronum >= onenum + twonum:
                                    st = []
                                    st.append(i)
                                    minnum = onenum
                                    mintwonum = twonum
                    else:
                        if zeronum >= onenum + twonum:
                            st = []
                            st.append(i)
                            minnum = onenum
                            mintwonum = twonum

    if 0 not in cardre[10:] and cardre[1] != 0:
        onenum = 0
        zeronum = 0
        twonum = 0
        for j in cardre[10:]:
            if j - 1 == 0:
                zeronum += 1
            if j - 1 == 1:
                onenum += 1
            if j - 1 == 2:
                twonum += 1
        if cardre[1] - 1 == 0:
            zeronum += 1
        if cardre[1] - 1 == 1:
            onenum += 1
        if cardre[1] - 1 == 2:
            twonum += 1
        if zeronum > onenum and minnum >= onenum:
            if len(st) == 0:

                if zeronum >= onenum + twonum:
                    st.append(10)
            else:

                if minnum == onenum:
                    if mintwonum >= twonum:
                        if zeronum >= onenum + twonum:
                            st = []
                            st.append(10)
                else:
                    if zeronum >= onenum + twonum:
                        st = []
                        st.append(10)

    tmp = []
    Flushtmp = []
    nowhandcards = []
    Straight = []
    if len(st) > 0:
        for i in range(st[0], st[0] + 5):
            if 1 < i < 10:
                Straight.append(str(i))
            if i % 13 == 1:
                Straight.append('A')
            if i == 10:
                Straight.append('T')
            if i == 11:
                Straight.append('J')
            if i == 12:
                Straight.append('Q')
            if i == 13:
                Straight.append('K')
    sttemp = []
    for i in range(4):
        sttemp.append([0] * 5)
    counttemp = 0

    colortemp = {"S": 0, "H": 1, "C": 2, "D": 3}
    rev_colortemp = {0: 'S', 1: 'H', 2: 'C', 3: 'D'}
    for i in range(0, len(handcards) - 1):
        if handcards[i][-1] in Straight:
            sttemp[colortemp[handcards[i][0]]][counttemp] += 1
            if handcards[i][-1] != handcards[i + 1][-1]:
                counttemp += 1

    StraightFlushflag = -1

    for i in range(4):
        if sttemp[i][0] > 0 and sttemp[i][1] > 0 and sttemp[i][2] > 0 and sttemp[i][3] > 0 and sttemp[i][4] > 0:
            StraightFlushflag = i
    if StraightFlushflag >= 0:
        for i in Straight:
            Flushtmp.append(rev_colortemp[StraightFlushflag] + i)
        for i in range(0, len(handcards)):
            if handcards[i] not in Flushtmp:
                nowhandcards.append(handcards[i])

    else:
        for i in range(0, len(handcards)):
            if handcards[i][-1] in Straight:
                tmp.append(handcards[i])
                Straight.remove(handcards[i][-1])
            else:
                nowhandcards.append(handcards[i])

    newcards = {}
    newcards["Single"] = []
    newcards["Pair"] = []
    newcards["Trips"] = []
    newcards["Bomb"] = []
    newcards['Straight'] = []
    newcards['StraightFlush'] = []

    if len(tmp) == 5:
        if tmp[-1][-1] == 'A' and tmp[-2][-1] == '5':
            tmpptmp = [tmp[-1]]
            for kkk in tmp[:-1]:
                tmpptmp.append(kkk)
            newcards['Straight'].append(tmpptmp)
        else:
            newcards['Straight'].append(tmp)
    if len(Flushtmp) == 5:
        newcards['StraightFlush'].append(Flushtmp)
    start = 0
    for i in range(1, len(nowhandcards) + 1):
        if i == len(nowhandcards) or nowhandcards[i][-1] != nowhandcards[i - 1][-1]:
            if (i - start == 1):
                newcards["Single"].append(nowhandcards[i - 1])
            elif (i - start == 2):
                newcards["Pair"].append(nowhandcards[start:i])
            elif (i - start) == 3:
                newcards["Trips"].append(nowhandcards[start:i])
            else:
                newcards["Bomb"].append(nowhandcards[start:i])
            start = i
    return newcards, bomb_info


    card_value_v2s = {0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8", 8: "9", 9: "T", 10: "J",
                      11: "Q", 12: "K"}
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}

    card_index = {"A": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10,
                  "Q": 11, "K": 12, "R": 13, "B": 13}
    new_remaincards = {}
    for key,val in remaincards.items():
        new_remaincards[key] = copy.deepcopy(val)
    for card in handcards:
        card_type = str(card[0])
        x = card_index[card[1]]
        new_remaincards[card_type][x] = remaincards[card_type][x]-1

    rest_cards = []

    for key,value in new_remaincards.items():
        for i  in range(0,len(value)):
            if value[i] ==0 :
                continue
            if i == 13 and key == 'S':
                val = 'B'
            elif i == 13 and key == 'H':
                val = 'R'
            else:
                val = card_value_v2s[i]
            if value[i]==1:
                rest_cards.append(key+val)
            elif value[i] == 2:
                rest_cards.append(key + val)
                rest_cards.append(key + val)
    if len(rest_cards)==0:
        print(rest_cards)
    card_value_s2v[str(rank)] = 15
    rest_cards = sorted(rest_cards,key = lambda item:card_value_s2v[item[1]])
    new_rest_cards = []
    tmp = []
    pre = rest_cards[0]
    tmp = [pre]
    for cards in rest_cards[1:]:
        if cards[1]!=pre[1]:
            new_rest_cards.append(tmp)
            tmp = [cards]
            pre = cards
        else:
            tmp.append(cards)
    new_rest_cards.append(tmp)
    return new_rest_cards