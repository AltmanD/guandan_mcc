import copy
def is_inStraight(action, straight_member):

    flag = 0
    print(straight_member)
    if len(straight_member) != 0:
        for card in action[2]:
            if card in straight_member:
                flag = 1
                break
    return flag

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
    for i in temp:
        if i[-1] == 'A':
            cardre[1] += 1
        if i[-1] == '2':
            cardre[2] += 1
        if i[-1] == '3':
            cardre[3] += 1
        if i[-1] == '4':
            cardre[4] += 1
        if i[-1] == '5':
            cardre[5] += 1
        if i[-1] == '6':
            cardre[6] += 1
        if i[-1] == '7':
            cardre[7] += 1
        if i[-1] == '8':
            cardre[8] += 1
        if i[-1] == '9':
            cardre[9] += 1
        if i[-1] == 'T':
            cardre[10] += 1
        if i[-1] == 'J':
            cardre[11] += 1
        if i[-1] == 'Q':
            cardre[12] += 1
        if i[-1] == 'K':
            cardre[13] += 1

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
                    minnum = onenum
                    mintwonum = twonum
            else:

                if minnum == onenum:
                    if mintwonum >= twonum:
                        if zeronum >= onenum + twonum:
                            st = []
                            st.append(10)
                            minnum = onenum
                            mintwonum = twonum
                else:
                    if zeronum >= onenum + twonum:
                        st = []
                        st.append(10)
                        minnum = onenum
                        mintwonum = twonum

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

def rest_cards(handcards,remaincards,rank):

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

def choose_bomb( bomb_actionList, handcards, sorted_cards, bomb_info, rank_card, card_val):
    new_card_val = copy.deepcopy(card_val)
    new_card_val['A'] = 14
    new_card_val[rank_card[1]] = 15
    bomb_res = []

    new_card_val["JOKER"] = 10000
    straight_member = []
    if len(sorted_cards["Straight"]) != 0:
        straight_member += sorted_cards["Straight"][0]
    if len(sorted_cards["StraightFlush"]) != 0:
        straight_member += sorted_cards["StraightFlush"][0]

    for action in bomb_actionList:

        index = action[0]
        action = action[1]
        if action[0] == "Bomb":
            if action[1]==rank_card[1]:
                prior = 0
                rank_card_num = 0
                for card in action[2]:
                    if card == rank_card:
                        rank_card_num += 1
                if rank_card_num == 1:
                    prior = 3
                elif rank_card_num == 2:
                    prior = 16
                l = len(action[2])
                bomb_res.append((index, new_card_val[action[1]] + (l - 4) * 16+prior))
            else:
                if action[1] in bomb_info:
                    if bomb_info[action[1]] == len(action[2]) and rank_card not in action[2]:
                        l = len(action[2])
                        bomb_res.append((index, new_card_val[action[1]] + (l - 4) * 16))
                    elif len(sorted_cards["Trips"])==0:
                        if len(action[2])>bomb_info[action[1]] and rank_card in action[2]:
                            l = len(action[2])
                            rank_card_num = len(action[2]) - bomb_info[action[1]]
                            prior = 0
                            if rank_card_num == 1:
                                prior = 3
                            elif rank_card_num == 2:
                                prior = 16
                            bomb_res.append((index, new_card_val[action[1]] + (l - 4) * 16+prior))

                elif action[1] not in bomb_info and rank_card in action[2]:
                    if is_inStraight(action, straight_member):
                        continue
                    prior = 0
                    rank_card_num = 0
                    for card in action[2]:
                        if card == rank_card:
                            rank_card_num += 1
                    if rank_card_num == 1:
                        prior = 3
                    elif rank_card_num == 2:
                        prior = 16
                    l = len(action[2])
                    bomb_res.append((index, new_card_val[action[1]] + (l - 4) * 16 + prior))
        elif action[0] == "StraightFlush":
            if len(sorted_cards["StraightFlush"]) > 0:
                curStraight = sorted_cards["StraightFlush"][0][0][1]
                if curStraight == action[1] and rank_card not in action[2]:
                    bomb_res.append((index, new_card_val[action[1]] + 32))

    if len(bomb_res) == 0:
        return -1
    else:
        bomb_res = sorted(bomb_res, key=lambda item: item[1])
        return bomb_res[0][0]

def one_hand(numofmy,numofnext,actionList,myPos,greaterPos,cards_num,restcards,card_val,rank_card):

    max_bomb = 0
    rank_card_num = 0
    for cards in restcards:
        if rank_card in cards:
            rank_card_num+=1
    for cards in restcards:
        if cards[0][1]==rank_card[1] and len(cards)>=4:
            l = len(cards)
            max_bomb = max(max_bomb,card_val[cards[0][1]]+(l-4)*14)
        elif cards[0][1]!=rank_card[1] and len(cards)>=4:
            l = len(cards)
            max_bomb = max(max_bomb, card_val[cards[0][1]] +(l+rank_card_num-4)*14)
        elif cards[0][1]!=rank_card[1] and len(cards)==3 and rank_card_num>=1:
            max_bomb = max(max_bomb, card_val[cards[0][1]] + (rank_card_num-1)*14)
        elif cards[0][1] != rank_card[1] and len(cards) == 2 and rank_card_num == 2:
            max_bomb = max(max_bomb, card_val[cards[0][1]])

    tag = 0
    if (myPos+2)%4 != greaterPos:
        for action in actionList[1:]:
            tag +=1
            if numofmy == len(action[2]):
                return tag
    else:
        for action in actionList[1:]:
            tag += 1
            if action[0]!="Bomb" and action[0]!="StraightFlush" and numofmy == len(action[2]):
                return tag
            if (action[0]=="Bomb" or action[0]=="StraightFlush") and numofmy == len(action[2]):

                if action[0]=="Bomb":
                    l = len(action[2])
                    cur_level = card_val[action[1]]+(l-4)*14
                else:
                    cur_level = card_val[action[1]] + 14
                if numofnext>cards_num and cur_level>max_bomb:
                    return 0
                else:
                    return tag

    return -1

def get_remain_card_type(remaincards,remaincards_classbynum):
    card_re = {}
    Single_type = []
    Pair_type = []
    Trips_type = []
    Bomb_type = []
    ThreePair_type = []
    TwoTrips_type= []
    Straight_type= []
    StraightFlush_type =[]
    for i in range(len(remaincards_classbynum)):
        if remaincards_classbynum[i]>= 4:
            Single_type.append(1)
            Bomb_type.append(1)
            Pair_type.append(1)
            continue
        else:
            Bomb_type.append(0)
        if  remaincards_classbynum[i]>= 3:
            Single_type.append(1)
            Trips_type.append(1)
            Pair_type.append(1)
            continue
        else:
            Trips_type.append(0)
        if  remaincards_classbynum[i]>= 2:
            Single_type.append(1)
            Pair_type.append(1)
            continue
        else:
            Pair_type.append(0)
        if  remaincards_classbynum[i]>= 1:
            Single_type.append(1)
        else:
            Single_type.append(0)
    #check Bomb
    Bomb_type =Bomb_type[:-2]
    if remaincards['H'][-1]==2 and remaincards['S'][-1]==2:
        Bomb_type.append(1)
    else:
        Bomb_type.append(0)
    card_re['Bomb'] =Bomb_type
    card_re['Pair'] = Pair_type
    card_re['Trips'] = Trips_type[:-2]
    card_re['Single'] = Single_type
    if len(Pair_type)>0:
        card_re['ThreeWithTwo'] = Trips_type[:-2]
    else:
        card_re['ThreeWithTwo'] = [0]*13
    for i in range(len(Pair_type)-3):
        if Pair_type[i]==1 and Pair_type[i+1]==1 and Pair_type[(i+2)%13] ==1:
            ThreePair_type.append(1)
        else:
            ThreePair_type.append(0)
    card_re['ThreePair'] =ThreePair_type
    for i in range(len(Trips_type)-2):
        if Trips_type[i]==1 and Trips_type[(i+1)%13]==1:
            TwoTrips_type.append(1)
        else:
            TwoTrips_type.append(0)
    card_re['TwoTrips'] =TwoTrips_type
    #check Straight
    for i in range(len(remaincards_classbynum) - 5):
        if remaincards_classbynum[i]>0 and remaincards_classbynum[i+1]>0 and remaincards_classbynum[i+2]>0 and remaincards_classbynum[i+3]>0 and remaincards_classbynum[(i+4)%13]>0 :
            Straight_type.append(0)
        else:
            Straight_type.append(1)
    card_re['Straight'] = Straight_type
    card_color = ['S','H','C','D']
    for i in range(len(Straight_type)):
        if Straight_type[i]==1:
            Straight_typeflag =0
            for j in card_color:
                if remaincards[j][i]>0 and remaincards[j][i+1]>0 and remaincards[j][i+2]>0 and remaincards[j][i+3]>0 and remaincards[j][(i+4)%13]>0:
                    StraightFlush_type.append(1)
                    Straight_typeflag =1
                    break
            if Straight_typeflag ==0:
                StraightFlush_type.append(0)
        else:
            StraightFlush_type.append(0)
    return card_re

def cal_bomb_num(sorted_cards,handcards,rank_card):
    cur_Bomb_num = len(sorted_cards["Bomb"]) + len(sorted_cards["StraightFlush"])
    rank_card_num = 0
    for card in handcards:
        if card == rank_card:
            rank_card_num += 1

    if rank_card_num == 1:
        for trip in sorted_cards["Trips"]:
            if rank_card not in trip:
                cur_Bomb_num += 1
                break
    if rank_card_num == 2:
        if len(sorted_cards["Trips"])==1 and rank_card not in sorted_cards["Trips"][0]:
            cur_Bomb_num += 1
        elif len(sorted_cards["Trips"])==2 and rank_card in sorted_cards["Trips"][1]:
            cur_Bomb_num += 1
        elif len(sorted_cards["Trips"])==2 and rank_card not in sorted_cards["Trips"][1]:
            cur_Bomb_num += 2
        elif len(sorted_cards["Trips"])>=2:
            cur_Bomb_num += 2

    for bomb in sorted_cards["Bomb"]:
        if rank_card in bomb:
            cur_Bomb_num -= 1

    return cur_Bomb_num

def combine_ThreePair(handcards,rank_card,sorted_cards,card_val):
    card_origin = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                   "Q": 12, "K": 13}
    card_val['A'] = 1
    card_val[rank_card[1]] = card_origin[rank_card[1]]
    Pairs = {}
    Trips = {}
    for pair in sorted_cards["Pair"]:
        Pairs[card_val[pair[0][1]]] = pair
    for trips in sorted_cards["Trips"]:
        Trips[card_val[trips[0][1]]] = trips

    for key,val in card_origin.items():
        if val >12 or val == 1:
            continue


def caldistance2(trips_actionlist,pair_actionlist,rank):
    rank_card = 'H' + str(rank)
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v[rank_card[-1]] = 15
    return card_value_s2v[trips_actionlist[0][0]],card_value_s2v[trips_actionlist[0][0]] - card_value_s2v[pair_actionlist[1][0]],card_value_s2v[pair_actionlist[1][0]],card_value_s2v[pair_actionlist[0][0]]

def caldistance3(trips_actionlist,pair_actionlist,rank):
    rank_card = 'H' + str(rank)
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v[rank_card[-1]] = 15
    return card_value_s2v[pair_actionlist[0][0]],card_value_s2v[trips_actionlist[0][0]] - card_value_s2v[pair_actionlist[0][0]],card_value_s2v[trips_actionlist[1][0]],card_value_s2v[trips_actionlist[0][0]]

def getindex(tag, actList, actionList):
    myaction = tag
    mynumber = actList[0][0]
    mycard = "None"
    if myaction == "Single":
        mycard = [actList[0][1]]
    else:
        mycard = actList[0][1]
    my_act = []
    my_act.append(myaction)
    my_act.append(mynumber)
    my_act.append(mycard)
    print(my_act)
    if my_act in actionList:
        return actionList.index(my_act)
    else:
        return 0

def getindex1(tag, actList, actionList):
    myaction = tag
    mynumber = actList[1][0]
    mycard = "None"
    if myaction == "Single":
        mycard = [actList[1][1]]
    else:
        mycard = actList[1][1]
    my_act = []
    my_act.append(myaction)
    my_act.append(mynumber)
    my_act.append(mycard)
    print(my_act)
    if my_act in actionList:
        return actionList.index(my_act)
    else:
        return 0

def rankfour(twotrips_actionlist,threepair_actionlist,actionList,cur2,cur3):#cur2是连对，cur3是连三

    card_value_s2v2 = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                       "Q": 12, "K": 13, "B": 16, "R": 17}
    minvalue = [100,100]

    if len(threepair_actionlist):
        minvalue[0] = card_value_s2v2[threepair_actionlist[0][0]]

    if len(twotrips_actionlist):
        minvalue[1] = card_value_s2v2[twotrips_actionlist[0][0]]

    minpos = minvalue.index(min(minvalue))
    if minpos == 0 and minvalue[0]<=cur2:
        return getindex("ThreePair",threepair_actionlist,actionList)

    if minpos == 1 and minvalue[1]<=cur3:
        return getindex("TwoTrips",twotrips_actionlist,actionList)

def rankthree(single_actionlist,pair_actionlist,trips_actionlist,threetwo_actionlist,actionList,numofnext,rank,cur1,cur4,cur5,cur6,curp2):
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v[rank] = 15
    if len(pair_actionlist) == len(trips_actionlist) or (
            len(pair_actionlist) >= 2 and len(trips_actionlist) >= 2):
        if card_value_s2v[threetwo_actionlist[0][0]] < cur4 or numofnext==1:
            return getindex("ThreeWithTwo",threetwo_actionlist,actionList)
        elif len(single_actionlist) and card_value_s2v[single_actionlist[0][0]] < cur1 and numofnext==5:
            return getindex("Single",single_actionlist,actionList)
        else:
            minvalue = [100, 100]
            if len(threetwo_actionlist):
                minvalue[0] = card_value_s2v[threetwo_actionlist[0][0]]

            if len(single_actionlist):
                minvalue[1] = card_value_s2v[single_actionlist[0][0]]

            if len(threetwo_actionlist)>1 and len(single_actionlist) == 1:#三带二有压
                minvalue[0] = minvalue[0] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0 :
                    return getindex("ThreeWithTwo", threetwo_actionlist, actionList)
                if minpos == 1 :
                    return getindex("Single", single_actionlist, actionList)
            elif len(threetwo_actionlist) == 1 and len(single_actionlist)>1:#单张有压
                minvalue[1] = minvalue[1] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0 :
                    return getindex("ThreeWithTwo", threetwo_actionlist, actionList)
                if minpos == 1 :
                    return getindex("Single", single_actionlist, actionList)
            else:
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("ThreeWithTwo", threetwo_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)

    else:
        len3 = len(pair_actionlist)
        len4 = len(trips_actionlist)

        if numofnext == 3 and len(pair_actionlist) and card_value_s2v[pair_actionlist[0][0]] < cur4:
            return getindex("Pair",pair_actionlist,actionList)
        if numofnext == 2 and len(trips_actionlist) and card_value_s2v[trips_actionlist[0][0]] < cur5:
            return getindex("ThreeWithTwo",threetwo_actionlist,actionList)

        if len3 > len4:
            mint,_,minp2,minp1= caldistance2(trips_actionlist,pair_actionlist,rank)
            if minp2 <= cur5 and mint <= cur6:
                if minp1 > mint:
                    return getindex("ThreeWithTwo",threetwo_actionlist,actionList)
                else:return getindex1("Pair",pair_actionlist,actionList)
            elif minp2 > cur5 and mint <= cur6:
                if minp2 > cur5 + curp2:
                    if minp1 < cur5:
                        return getindex("Pair",pair_actionlist,actionList)
                    else:
                        return getindex("ThreeWithTwo",threetwo_actionlist,actionList)
                else:
                    return getindex("ThreeWithTwo",threetwo_actionlist,actionList)
            elif minp2 <= cur5 and mint > cur6:
                return getindex("Pair",pair_actionlist,actionList)
            else:
                return getindex("ThreeWithTwo",threetwo_actionlist,actionList)

        else:
            minp, _, mint2, mint1 = caldistance3(trips_actionlist, pair_actionlist, rank)
            if minp <= cur5:
                return getindex("ThreeWithTwo",threetwo_actionlist,actionList)
            elif mint1 < cur6 and minp > cur5:
                return getindex("Trips",trips_actionlist,actionList)
            else:
                if minp >= cur5 + curp2:
                    return getindex("Trips",trips_actionlist,actionList)
                else:
                    return getindex("ThreeWithTwo",threetwo_actionlist,actionList)


def ranktwo(hand_cards,single_actionlist,pair_actionlist,trips_actionlist,actionList,numofnext,rank,max_val):
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v[rank] = 15
    rank_card = 'H'+rank
    if len(single_actionlist):
        if numofnext == 1:
            return getindex("Pair", pair_actionlist, actionList)
        if numofnext == 2:
            return getindex("Single",single_actionlist,actionList)
        else:
            minvalue = [100, 100]
            if len(pair_actionlist):
                minvalue[0] = card_value_s2v[pair_actionlist[0][0]]

            if len(single_actionlist):
                minvalue[1] = card_value_s2v[single_actionlist[0][0]]

            if len(pair_actionlist) > 1 and len(single_actionlist) == 1:
                minvalue[0] = minvalue[0] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Pair", pair_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
            elif len(pair_actionlist) == 1 and len(single_actionlist) > 1:
                minvalue[1] = minvalue[1] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Pair", pair_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
            else:
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Pair", pair_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
    else:
        return getindex("Pair", pair_actionlist, actionList)


def rankone(single_actionlist,trips_actionlist,actionList,numofnext,rank):
    card_value_s2v = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                      "Q": 12, "K": 13, "A": 14, "B": 16, "R": 17}
    card_value_s2v[rank] = 15
    if len(single_actionlist):
        if numofnext == 1:
            return getindex("Trips", trips_actionlist, actionList)
        if numofnext == 3:
            return getindex("Single", single_actionlist, actionList)
        else:
            minvalue = [100, 100]
            if len(trips_actionlist):
                minvalue[0] = card_value_s2v[trips_actionlist[0][0]]

            if len(single_actionlist):
                minvalue[1] = card_value_s2v[single_actionlist[0][0]]

            if len(trips_actionlist) > 1 and len(single_actionlist) == 1:  # 三带二有压
                minvalue[0] = minvalue[0] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Trips", trips_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
            elif len(trips_actionlist) == 1 and len(single_actionlist) > 1:  # 单张有压
                minvalue[1] = minvalue[1] + 1
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Trips", trips_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
            else:
                minpos = minvalue.index(min(minvalue))
                if minpos == 0:
                    return getindex("Trips", trips_actionlist, actionList)
                if minpos == 1:
                    return getindex("Single", single_actionlist, actionList)
    else:
        return getindex("Trips", trips_actionlist, actionList)