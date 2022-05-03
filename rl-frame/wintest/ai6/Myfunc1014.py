class Myfunc1014(object):
    def firstcard(self,hd, cur):
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R']
        poke.remove(cur)
        poke.insert(12,cur)
        hdcopy = hd[:]
        num = 0
        dict = {'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [], 'TwoTrips': [],
                'ThreeWithTwo': [],'Straight': [], 'Bomb': [], 'StraightFlush': [], 'numh': [],
                }
        # 寻找红桃配
        for i in hdcopy:
            #print(i)
            if i.find(cur) == 1 and i[0] == 'H':
                dict['numh'].append(i)
        # print(len(self.getcard(hdcopy, dict['numh'])['Straight'][1]))
        while len(self.getcard(hdcopy, dict['numh'])['Straight']) > 0:
            # print("长度",len(getcard(hdcopy))['Straight'][1::2])
            #print("getcard的顺子", self.getcard(hdcopy, dict['numh'])['Straight'])
            dict['Straight'].append(self.getcard(hdcopy, dict['numh'])['Straight'][0][1])
            dict['Straight'].append(self.getcard(hdcopy, dict['numh'])['Straight'])
            for i in self.getcard(hdcopy, dict['numh'])['Straight']:
              #  print(i)
                hdcopy.remove(i)
                if dict['numh'].count(i)>0:
                    dict['numh'].remove(i)
                # 红桃配

        dict['Bomb'] = self.getcard(hdcopy,dict['numh'])['Boom']
        print(dict['Bomb'])
        if len(dict['Bomb']) > 0:
            for i in dict['Bomb'][1::2]:
                for j in i:
                    if poke.index(j[1]) <= 12:
                        hdcopy.remove(j)
        # print("这是hdcopy", hdcopy)
        tpcopy=dict['Trips']
        dict['TwoTrips'] = self.getcard(hdcopy, dict['numh'])['TwoTrips']
        print(dict['TwoTrips'])
        if len(dict['TwoTrips']) > 0:
             for i in dict['TwoTrips'][1::2]:
                for j in i:
                    if poke.index(j[1]) <=8:
                        hdcopy.remove(j)
        dict['ThreePair'] = self.getcard(hdcopy, dict['numh'])['ThreePair']
        #print("这是先手配的连对",dict['ThreePair'])
        if len(dict['ThreePair']) > 0:
            for i in dict['ThreePair'][1::2]:
                for j in i:
                    if poke.index(j[1])<=10:
                        #print("这是j",j,j[1],poke.index(j[1]))
                        hdcopy.remove(j)
       # print("这是hdcopy", hdcopy)
        print("这是dict",dict)
        dict['Single']=[]
        dict['Pair']=[]
        dict['Trips']=[]
        print("这是先手配的牌",dict)
        return (hdcopy, dict)

    def getcard(self,hd, numh):
        poke = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'B', 'R']
        pn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dict = {'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [], 'TwoTrips': [],
                'ThreeWithTwo': [],  'Straight': [], 'Boom': [], 'StraightFlush': [], 'numh': [],'boom':[]}
        lnumh = len(numh)
        #print("有", lnumh, "个红桃配")
        colorlist = []  # 花色的牌
        sg = []  # 顺子
        str = []
        num = 0
        twt = []  # 三单二初始表格
        for i in poke:
            list = 0
            colorlist = []
            for j in hd:
                if j.find(i) == 1:
                    list = i
                    colorlist.append(j)
            sg.append(list)
            if list == 0 or list == 'k':
                # if len(sg)>=5:
                #   str.append(sg)
                sg = []
            elif len(colorlist) == 1:
                dict['Single'].append(i)
                dict['Single'].append(colorlist)
            elif len(colorlist) == 2:
                dict['Pair'].append(i)
                dict['Pair'].append(colorlist)
            elif len(colorlist) == 3 and lnumh > 0 and i!=numh[0][1]:
                lnumh -= 1
                dict['Boom'].append(i)
                colorlist.append(numh[0])
                dict['Boom'].append(colorlist)
            elif len(colorlist) == 3:
                dict['Trips'].append(i)
                dict['Trips'].append(colorlist)
            elif len(colorlist) >= 4:
                dict['boom'].append(i)
                dict['boom'].append(colorlist)
            # elif len(colorlist)>=4:
        #    dict['Boom'].append(i)
        #   dict['Boom'].append(colorlist)
        # 寻找三带二
        if len(dict['Trips']) > 0 and len(dict['Pair']) > 0:
            for i in dict['Trips'][::2]:
                dict['ThreeWithTwo'].append(i)
                twt = dict['Trips'][dict['Trips'].index(i) + 1] + dict['Pair'][1]
                dict['ThreeWithTwo'].append(twt)
        # 配顺子
        # 寻找连对

        # 寻找顺子
        #print(dict['Straight'])
        dict['Straight'] = self.lgetsunzi(dict)
        dict['ThreePair'] += self.getliandui(dict)
        dict['TwoTrips']+=self.lgetttr(dict)
        # print(hd)
        # 寻找同花顺
        return dict

    def lgetsunzi(self,dict):
        poke = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        pair = dict['Pair'][::2]
        trip = dict['Trips'][::2]
        single = dict['Single'][::2]
        bomb = dict['boom'][::2]
        # len=len(numh)
        eb = []
        sunzi = []
        clsz = []
        lastcl = []
        num = 0
        maxnum = 0
        while (len(poke) >= 6):
            cl = []
            eb = []
            num = 0
            for i in poke:
                if pair.count(i) == 1 or trip.count(i) == 1 or single.count(i) == 1 or bomb.count(i) == 1:
                    eb.append(i)
                    if len(eb) >= 5:
                       # print("这是eb", eb, num)
                        for i in eb:
                            if single.count(i) == 1:
                                cl += dict['Single'][dict['Single'].index(i) + 1]
                                num += 1
                                #print("这是eb", eb, num)
                            elif pair.count(i) == 1:
                                cl.append(dict['Pair'][dict['Pair'].index(i) + 1][0])
                                # print(dict['Pair'][dict['Pair'].index(i)+1][0])
                                num -= 1
                               # print("这是eb", eb, num)
                            elif trip.count(i) == 1:
                                cl.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                                num -= 1
                               # print("这是eb", eb, num)
                            elif bomb.count(i) == 1:
                                cl.append(dict['boom'][dict['boom'].index(i) + 1][0])
                                num -= 2
                              #  print("这是eb", eb, num)
                        if num >= 0 and num > maxnum:
                            maxnum = num
                            #print(maxnum)
                            sunzi = cl
                            num = 0
                            eb = []
                            cl = []
                        else:
                            num = 0
                            eb = []
                            cl = []

                else:
                    eb = []
                    num = 0
                    cl = []
            poke.remove(poke[0])
        return sunzi
    def lgetliandui(self, dict):
        poke = ['A','2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q']
        pair = dict['Pair'][::2]
        trip = dict['Trips'][::2]
        ez = []
        cldui = []
        dui = []
        num = 0
        for i in poke:
            if pair.count(i) == 1 or trip.count(i) == 1:
                ez.append(i)
                if len(ez) >= 3:
                    for i in ez:
                        if pair.count(i) == 1:
                            cldui.append(dict['Pair'][dict['Pair'].index(i) + 1][0])
                            cldui.append(dict['Pair'][dict['Pair'].index(i) + 1][1])
                            num += 1
                        else:
                            cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                            cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][1])
                            num -= 1
                    if num == 3:
                        dui.append(cldui[0][1])
                        dui.append(cldui)
                        cldui = []
                        ez = []
                        num = 0
                    else:
                        cldui = []
                        ez = []
                        num = 0
            else:
                cldui = []
                ez = []
                num = 0
        #print("这是连对",dui)
        return dui
    def lgetttr(self,dict):
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'B', 'R']
        trip = dict['Trips'][::2]
        ez = []
        cldui = []
        dui = []
        num = 0
        for i in poke:
            if trip.count(i) == 1:
                ez.append(i)
                if len(ez) >= 2:
                    #print(ez)
                    for i in ez:
                        #print(dict['Trips'][dict['Trips'].index(i) + 1][0])
                        #print(dict['Trips'][dict['Trips'].index(i) + 1][1])
                        cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                        cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][1])
                        cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][2])
                        #print(cldui)
                        if len(cldui) >= 5:
                            dui.append(cldui[0][1])
                            dui.append(cldui)
                    cldui = []
                    ez = []
            else:
                cldui = []
                ez = []
        #print("这是钢板", dui)
        return dui

    def lgetcard(self,hd,dict):
        poke = [ '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K','A', 'B', 'R']
        pn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        colorlist = []  # 花色的牌
        sg = []  # 顺子
        str = []
        num = 0
        twt = []  # 三单二初始表格
        # dict = {'ThreeWithTwo': [],'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [],
        #          'ThreePair': [], 'Straight': [], 'Bomb': [], 'StraightFlush': []}
        for i in poke:
            list = 0
            colorlist = []
            for j in hd:
                if j.find(i) == 1:
                    list = i
                    colorlist.append(j)
            sg.append(list)
            if list == 0 or list == 'k':
                # if len(sg)>=5:
                #   str.append(sg)
                sg = []
            elif len(colorlist) == 1:
                dict['Single'].append(i)
                dict['Single'].append(colorlist)
            elif len(colorlist) == 2:
                dict['Pair'].append(i)
                dict['Pair'].append(colorlist)
            elif len(colorlist) == 3:
                dict['Trips'].append(i)
                dict['Trips'].append(colorlist)
            elif len(colorlist) >= 4:
                dict['Bomb'].append(i)
                dict['Bomb'].append(colorlist)
        # 寻找三带二
        if len(dict['Trips']) > 0 and len(dict['Pair']) > 0 and poke.index(dict['Pair'][0])<11:
            for i in dict['Trips'][::2]:
                dict['ThreeWithTwo'].append(i)
                twt = dict['Trips'][dict['Trips'].index(i) + 1] + dict['Pair'][1]
                dict['ThreeWithTwo'].append(twt)
        # 配顺子
        dict['Straight']+= self.getsunzi(dict)
        # 寻找连对
        dict['ThreePair']+= self.getliandui(dict)
        #寻找钢板
        # 寻找顺子
        # 寻找同花顺
        # dict['Trips']=[]
        return dict

    def getsunzi(self, dict):
        poke = ['A','2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        pair = dict['Pair'][::2]
        trip = dict['Trips'][::2]
        single = dict['Single'][::2]
        eb = []
        sunzi = []
        clsz = []
        lastcl = []
        num = 0
        while (len(poke) >= 6):
            cl = []
            eb = []
            num = 0
            for i in poke:
                if pair.count(i) == 1 or trip.count(i) == 1 or single.count(i) == 1:
                    eb.append(i)
                    if len(eb) >= 5:
                        for i in eb:
                            if single.count(i) == 1:
                                cl += dict['Single'][dict['Single'].index(i) + 1]
                                num += 1
                            else:
                                if pair.count(i) == 1:
                                    cl.append(dict['Pair'][dict['Pair'].index(i) + 1][0])
                                elif trip.count(i) == 1:
                                    cl.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                                num -= 1
                        if num > 0:
                            sunzi.append(eb)
                            clsz.append(cl)
                            num = 0
                            eb = []
                            cl = []
                        else:
                            num = 0
                            eb = []
                            cl = []

                else:
                    eb = []
                    num = 0
                    cl = []
            poke.remove(poke[0])
        for i in clsz:
            if i not in lastcl:
                lastcl.append(clsz[clsz.index(i)][0][1])
                lastcl.append(i)
        return lastcl

    def getliandui(self, dict):
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        pair = dict['Pair'][::2]
        trip = dict['Trips'][::2]
        ez = []
        cldui = []
        dui = []
        num = 0
        for i in poke:
            if pair.count(i) == 1 or trip.count(i) == 1:
                ez.append(i)
                if len(ez) >= 3:
                    for i in ez:
                        if pair.count(i) == 1:
                            cldui.append(dict['Pair'][dict['Pair'].index(i) + 1][0])
                            cldui.append(dict['Pair'][dict['Pair'].index(i) + 1][1])
                            num += 1
                        else:
                            cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                            cldui.append(dict['Trips'][dict['Trips'].index(i) + 1][1])
                            num -= 1
                    if num >= 0:
                        dui.append(cldui[0][1])
                        dui.append(cldui)
                        cldui = []
                        ez = []
                        num = 0
                    else:
                        cldui = []
                        ez = []
                        num = 0
            else:
                cldui = []
                ez = []
                num = 0
        return dui
    #配钢板
    def getcolor(self, dict, cur):
        print("getcolordict",dict)
        index = []
        len1=0
        min = 99
        ls = []
        getnum1 = self.getnumb(dict, cur)
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        poker.remove(cur)
        poker.insert(12, cur)
        if len(dict['Straight']):
            for i in dict['Straight'][1::2]:
                # print(i)
                ls.append([i])
                # print(ls[0])
                print("先手出了顺子",ls[0])
            return ls[0][0]
        if len(dict['ThreePair']) and poker.index(dict['ThreePair'][0])<=10:
           #print("这是连对",dict['ThreePair'])
            for i in dict['ThreePair'][1::2]:
                #print(dict['ThreePair'][1::2])
                ls.append([i])
               # print(ls[0])
                print("先手出了连对",ls[0])
            return ls[0][0]
        if len(dict['TwoTrips']) and poker.index(dict['TwoTrips'][0])<=8:
            #print("这是钢板",dict['TwoTrips'])
            for i in dict['TwoTrips'][1::2]:
               # print(dict['TwoTrips'][1::2])
                ls.append([i])
               # print(ls[0])
                print("先手出了钢板",ls[0])
            return ls[0][0]
        if len(dict['Single']) != 0 and getnum1[0] and getnum1[1] >= 2:
            print("我先出了单张")
            for i in dict['Single'][1::2]:
                ls.append([i])
            return ls[0][0]
        if len(dict['ThreeWithTwo']) and poker.index(dict['ThreeWithTwo'][0])<=9:
            for i in dict['ThreeWithTwo'][1::2]:
                # print(i)
                ls.append([i])
                # print(ls[0])
                print("先手出了三带二",ls[0])
            return ls[0][0]
        if len(dict['Trips']) and poker.index(dict['Trips'][0])<=9:
            for i in dict['Trips'][1::2]:
                # print(i)
                ls.append([i])
                # print(ls[0])
                print("先手出了三zhang",ls[0])
            return ls[0][0]
        else:
            for i in dict:
                if len(dict[i])>len1:
                    len1=len(dict[i])
                    ls=dict[i][1::2]
       # print(ls[0])
        return ls[0]

    def getcolor2(self,dict, cur, typec):
        index = []
        len1 = 0
        min = 99
        ls = []
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R', 'JOKER']
        poker.remove(cur)
        poker.insert(12, cur)
        if len(dict['Straight']):
            for i in dict['Straight'][1::2]:
                # print(i)
                ls.append([i])
                # print(ls[0])
            return ls[0][0]
        else:
            for i in list(dict):
                if i == typec:
                    print(i)
                    del dict[typec]
                else:
                    if len(dict[i]) > len1:
                        len1 = len(dict[i])
                        ls = dict[i][1::2]
        return ls[0]

    def getindex(self,actionlist,color):
        index=0
        for i in actionlist:
            if color==i[2]:
                index=actionlist.index(i)
        return  index

    def reSort2(self,curRank, getNum):
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        poker.remove(curRank)
        poker.insert(12, curRank)
        if poker.index(getNum) > poker.index('A'):
            return 1
        else:
            return 0

    def reSort3(self, curRank, getNum):
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        poker.remove(curRank)
        poker.insert(12, curRank)
        if poker.index(getNum) < poker.index('A'):
            return 1
        else:
            return 0

    def reSortun9(self, curRank, getNum):
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        poker.remove(curRank)
        poker.insert(12, curRank)
        if poker.index(getNum) > poker.index('9'):
            return 1
        else:
            return 0

    def reSortunQ(self, curRank, getNum):
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        poker.remove(curRank)
        poker.insert(12, curRank)
        if poker.index(getNum) > poker.index('Q'):
            return 1
        else:
            return 0

    def under6_total(self,list2):
        j = 0
        for i in range(len(list2)):
            if list2[i] <= 6:
                j = j + 1
        return j

    # 返回一个列表中第二小的数
    def secondmin2(self,list26):
        list26 = sorted(list26, reverse=True)
        return list26[-2]

    #返回一个列表中第三小的数
    def thirdmin(self,list26):
        list26 = sorted(list26, reverse=True)
        return list26[-3]

    # 返回一个列表中第四小的数
    def forthmin(self,list26):
        list26 = sorted(list26, reverse=True)
        return list26[-4]

    def search_color(self,hd, anycard):
        single = []
        for i in hd:
            for j in anycard:
                if i.find(j) == 1:
                    single.append(i)
        return single

    def getnumb(self, dict2, cur):
        numc = []
        for i in range(int(len(dict2['Single']) / 2)):
            numc.append(dict2['Single'][2 * i])
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R', 'JOKER']
        poker.remove(cur)
        poker.insert(12, cur)
        a = 0
        b = 0
        c = 0
        for i in range(len(numc)):
            if poker.index(numc[i]) >= 10:
                a = a + 1
            else:
                b = b + 1
        for i in range(len(numc)):
            if poker.index(numc[i]) <= 7:
                c = c + 1
        if a >= b:
            return 1, c
        else:
            return 0, c
# lasthand=Myfunc1014()
# data= {'type': 'act', 'stage': 'play', 'handCards': ['H2', 'H2', 'C4', 'H5', 'H5', 'D5', 'D6', 'S7', 'S7', 'C7', 'C7', 'D7', 'S8', 'S8', 'C8', 'H9', 'CT', 'DT', 'SQ', 'CQ', 'DQ', 'DK', 'DA', 'HJ', 'CJ', 'DJ', 'SB'], 'publicInfo': [{'rest': 8, 'playArea': [None, None, None]}, {'rest': 11, 'playArea': ['PASS', 'PASS', 'PASS']}, {'rest': 15, 'playArea': ['PASS', 'PASS', 'PASS']}, {'rest': 2, 'playArea': [None, None, None]}], 'selfRank': '2', 'oppoRank': '2', 'curRank': '2', 'curPos': -1, 'curAction': [None, None, None], 'greaterPos': -1, 'greaterAction': [None, None, None], 'actionList': [['Single', '4', ['H4']], ['Single', '4', ['C4']], ['Single', '5', ['S5']], ['Single', '6', ['D6']], ['Single', '7', ['S7']], ['Single', '2', ['C2']], ['Single', 'B', ['SB']], ['Pair', '4', ['H4', 'C4']], ['Pair', '2', ['C2', 'C2']]], 'indexRange': 8}
# hd=data['handCards']
# lh=lasthand
# # dit=lh.getcard(hd)
# # print(lh.getcard(hd))
# msg={'type': 'act', 'stage': 'play',
#      'handCards':
#          ['H4', 'C4', 'D5', 'S6', 'H6', 'C6', 'D6', 'H7', 'D8', 'D9', 'D9', 'ST', 'HT', 'CT', 'DT', 'SJ', 'DJ', 'CQ', 'CQ', 'CK', 'SA', 'HA', 'CA', 'CA', 'S2', 'H2', 'C2'], 'publicInfo': [{'rest': 27, 'playArea': None}, {'rest': 27, 'playArea': None}, {'rest': 27, 'playArea': None}, {'rest': 27, 'playArea': None}], 'selfRank': '2', 'oppoRank': '2', 'curRank': '2', 'curPos': -1, 'curAction': [None, None, None], 'greaterPos': -1, 'greaterAction': [None, None, None], 'actionList': [['Single', '4', ['H4']], ['Single', '4', ['C4']], ['Single', '5', ['D5']], ['Single', '6', ['S6']], ['Single', '6', ['H6']], ['Single', '6', ['C6']], ['Single', '6', ['D6']], ['Single', '7', ['H7']], ['Single', '8', ['D8']], ['Single', '9', ['D9']], ['Single', 'T', ['ST']], ['Single', 'T', ['HT']], ['Single', 'T', ['CT']], ['Single', 'T', ['DT']], ['Single', 'J', ['SJ']], ['Single', 'J', ['DJ']], ['Single', 'Q', ['CQ']], ['Single', 'K', ['CK']], ['Single', 'A', ['SA']], ['Single', 'A', ['HA']], ['Single', 'A', ['CA']], ['Single', '2', ['S2']], ['Single', '2', ['H2']], ['Single', '2', ['C2']], ['Pair', '4', ['H4', 'H2']], ['Pair', '4', ['H4', 'C4']], ['Pair', '4', ['C4', 'H2']], ['Pair', '5', ['D5', 'H2']], ['Pair', '6', ['S6', 'H2']], ['Pair', '6', ['S6', 'D6']], ['Pair', '6', ['S6', 'C6']], ['Pair', '6', ['S6', 'H6']], ['Pair', '6', ['H6', 'H2']], ['Pair', '6', ['H6', 'D6']], ['Pair', '6', ['H6', 'C6']], ['Pair', '6', ['C6', 'H2']], ['Pair', '6', ['C6', 'D6']], ['Pair', '6', ['D6', 'H2']], ['Pair', '7', ['H7', 'H2']], ['Pair', '8', ['D8', 'H2']], ['Pair', '9', ['D9', 'H2']], ['Pair', '9', ['D9', 'D9']], ['Pair', 'T', ['ST', 'H2']], ['Pair', 'T', ['ST', 'DT']], ['Pair', 'T', ['ST', 'CT']], ['Pair', 'T', ['ST', 'HT']], ['Pair', 'T', ['HT', 'H2']], ['Pair', 'T', ['HT', 'DT']], ['Pair', 'T', ['HT', 'CT']], ['Pair', 'T', ['CT', 'H2']], ['Pair', 'T', ['CT', 'DT']], ['Pair', 'T', ['DT', 'H2']], ['Pair', 'J', ['SJ', 'H2']], ['Pair', 'J', ['SJ', 'DJ']], ['Pair', 'J', ['DJ', 'H2']], ['Pair', 'Q', ['CQ', 'H2']], ['Pair', 'Q', ['CQ', 'CQ']], ['Pair', 'K', ['CK', 'H2']], ['Pair', 'A', ['SA', 'H2']], ['Pair', 'A', ['SA', 'CA']], ['Pair', 'A', ['SA', 'HA']], ['Pair', 'A', ['HA', 'H2']], ['Pair', 'A', ['HA', 'CA']], ['Pair', 'A', ['CA', 'H2']], ['Pair', 'A', ['CA', 'CA']], ['Pair', '2', ['S2', 'C2']], ['Pair', '2', ['S2', 'H2']], ['Pair', '2', ['H2', 'C2']], ['Trips', '4', ['H4', 'C4', 'H2']], ['Trips', '6', ['S6', 'H6', 'H2']], ['Trips', '6', ['S6', 'H6', 'D6']], ['Trips', '6', ['S6', 'H6', 'C6']], ['Trips', '6', ['S6', 'C6', 'H2']], ['Trips', '6', ['S6', 'C6', 'D6']], ['Trips', '6', ['S6', 'D6', 'H2']], ['Trips', '6', ['H6', 'C6', 'H2']], ['Trips', '6', ['H6', 'C6', 'D6']], ['Trips', '6', ['H6', 'D6', 'H2']], ['Trips', '6', ['C6', 'D6', 'H2']], ['Trips', '9', ['D9', 'D9', 'H2']], ['Trips', 'T', ['ST', 'HT', 'H2']], ['Trips', 'T', ['ST', 'HT', 'DT']], ['Trips', 'T', ['ST', 'HT', 'CT']], ['Trips', 'T', ['ST', 'CT', 'H2']], ['Trips', 'T', ['ST', 'CT', 'DT']], ['Trips', 'T', ['ST', 'DT', 'H2']], ['Trips', 'T', ['HT', 'CT', 'H2']], ['Trips', 'T', ['HT', 'CT', 'DT']], ['Trips', 'T', ['HT', 'DT', 'H2']], ['Trips', 'T', ['CT', 'DT', 'H2']], ['Trips', 'J', ['SJ', 'DJ', 'H2']], ['Trips', 'Q', ['CQ', 'CQ', 'H2']], ['Trips', 'A', ['SA', 'HA', 'H2']], ['Trips', 'A', ['SA', 'HA', 'CA']], ['Trips', 'A', ['SA', 'CA', 'H2']], ['Trips', 'A', ['SA', 'CA', 'CA']], ['Trips', 'A', ['HA', 'CA', 'H2']], ['Trips', 'A', ['HA', 'CA', 'CA']], ['Trips', 'A', ['CA', 'CA', 'H2']], ['Trips', '2', ['S2', 'H2', 'C2']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'S6', 'D6']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'S6', 'C6']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'S6', 'H6']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'H6', 'D6']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'H6', 'C6']], ['ThreePair', '4', ['H4', 'C4', 'D5', 'H2', 'C6', 'D6']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'ST', 'DT']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'ST', 'CT']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'ST', 'HT']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'HT', 'DT']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'HT', 'CT']], ['ThreePair', '8', ['D8', 'H2', 'D9', 'D9', 'CT', 'DT']], ['ThreePair', '9', ['D9', 'H2', 'ST', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'H2', 'ST', 'CT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'H2', 'ST', 'HT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'H2', 'HT', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'H2', 'HT', 'CT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'H2', 'CT', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'H2', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'DT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'DT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'CT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'CT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'CT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'HT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'HT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'ST', 'HT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'H2', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'DT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'DT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'CT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'CT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'HT', 'CT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'CT', 'H2', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'CT', 'DT', 'SJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'CT', 'DT', 'SJ', 'DJ']], ['ThreePair', '9', ['D9', 'D9', 'CT', 'DT', 'DJ', 'H2']], ['ThreePair', '9', ['D9', 'D9', 'DT', 'H2', 'SJ', 'DJ']], ['ThreePair', 'T', ['ST', 'H2', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'DT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'DT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['ST', 'DT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'DT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'CT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'CT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['ST', 'CT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'CT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'HT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'HT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['ST', 'HT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['ST', 'HT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'H2', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'DT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'DT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['HT', 'DT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'DT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'CT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'CT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['HT', 'CT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['HT', 'CT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['CT', 'H2', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['CT', 'DT', 'SJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['CT', 'DT', 'SJ', 'DJ', 'CQ', 'H2']], ['ThreePair', 'T', ['CT', 'DT', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'T', ['CT', 'DT', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreePair', 'T', ['DT', 'H2', 'SJ', 'DJ', 'CQ', 'CQ']], ['ThreePair', 'J', ['SJ', 'DJ', 'CQ', 'CQ', 'CK', 'H2']], ['ThreePair', 'Q', ['CQ', 'CQ', 'CK', 'H2', 'SA', 'CA']], ['ThreePair', 'Q', ['CQ', 'CQ', 'CK', 'H2', 'SA', 'HA']], ['ThreePair', 'Q', ['CQ', 'CQ', 'CK', 'H2', 'HA', 'CA']], ['ThreePair', 'Q', ['CQ', 'CQ', 'CK', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'S6', 'D6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'S6', 'C6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'S6', 'H6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'H6', 'D6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'H6', 'C6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'C6', 'D6']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '4', ['H4', 'C4', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'H4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'C4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'D5', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'H7', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'D8', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'D9', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'ST', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'HT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'DT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'SJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'DJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CQ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CK', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'SA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'HA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'S2', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'D6', 'H2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'H4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'C4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'D5', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'H7', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'D8', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'D9', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'ST', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'HT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'DT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'SJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'DJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CQ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CK', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'SA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'HA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'S2', 'H2']], ['ThreeWithTwo', '6', ['S6', 'H6', 'C6', 'H2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'H4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'C4', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'D5', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'H7', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'D8', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'D9', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'ST', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'HT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'DT', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'SJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'DJ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CQ', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CK', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'SA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'HA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CA', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'S2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'S2', 'H2']], ['ThreeWithTwo', '6', ['S6', 'C6', 'D6', 'H2', 'C2']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['S6', 'D6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'H4', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'H4', 'C4']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'C4', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'D5', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'H7', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'D8', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'D9', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'D9', 'D9']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'ST', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'ST', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'ST', 'CT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'ST', 'HT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'HT', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'HT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'HT', 'CT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CT', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'DT', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'SJ', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'DJ', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CQ', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CK', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'SA', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'SA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'SA', 'HA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'HA', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'HA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CA', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'CA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'S2', 'C2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'S2', 'H2']], ['ThreeWithTwo', '6', ['H6', 'C6', 'D6', 'H2', 'C2']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['H6', 'D6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'D9', 'D9']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '6', ['C6', 'D6', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'H4', 'C4']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'S6', 'D6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'S6', 'C6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'S6', 'H6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'H6', 'D6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'H6', 'C6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'C6', 'D6']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'ST', 'DT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'ST', 'CT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'ST', 'HT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'HT', 'DT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'HT', 'CT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'CT', 'DT']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'SA', 'CA']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'SA', 'HA']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'HA', 'CA']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'CA', 'CA']], ['ThreeWithTwo', '9', ['D9', 'D9', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'C4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'D5', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'C6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'D6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H7', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'D8', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'D9', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'SJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'DJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'CQ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'CK', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'SA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'HA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'CA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'S2', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'DT', 'H2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'C4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'D5', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'C6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'D6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H7', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'D8', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'D9', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'SJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'DJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'CQ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'CK', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'SA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'HA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'CA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'S2', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'HT', 'CT', 'H2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'C4', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'D5', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'C6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'D6', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H7', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'D8', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'D9', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'SJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'DJ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'CQ', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'CK', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'SA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'HA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'CA', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'S2', 'H2']], ['ThreeWithTwo', 'T', ['ST', 'CT', 'DT', 'H2', 'C2']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['ST', 'DT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H4', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'C4', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'D5', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S6', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H6', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'C6', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'D6', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H7', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'D8', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'D9', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'SJ', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'DJ', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'CQ', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'CK', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'SA', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'HA', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'CA', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'S2', 'H2']], ['ThreeWithTwo', 'T', ['HT', 'CT', 'DT', 'H2', 'C2']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['HT', 'DT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'T', ['CT', 'DT', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'J', ['SJ', 'DJ', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'SA', 'CA']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'SA', 'HA']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'HA', 'CA']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'CA', 'CA']], ['ThreeWithTwo', 'Q', ['CQ', 'CQ', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H4', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'C4', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'D5', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'C6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'D6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H7', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'D8', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'D9', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'ST', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'HT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'CT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'DT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'SJ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'DJ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'CQ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'CK', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'S2', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'HA', 'CA', 'H2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H4', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'C4', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'D5', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'C6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'D6', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H7', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'D8', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'D9', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'ST', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'HT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'CT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'DT', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'SJ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'DJ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'CQ', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'CK', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'S2', 'H2']], ['ThreeWithTwo', 'A', ['SA', 'CA', 'CA', 'H2', 'C2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'H2', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H4', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'C4', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'D5', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S6', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H6', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'C6', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'D6', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H7', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'D8', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'D9', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'ST', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'HT', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'CT', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'DT', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'SJ', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'DJ', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'CQ', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'CK', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S2', 'C2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'S2', 'H2']], ['ThreeWithTwo', 'A', ['HA', 'CA', 'CA', 'H2', 'C2']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'H4', 'C4']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'S6', 'D6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'S6', 'C6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'S6', 'H6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'H6', 'D6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'H6', 'C6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'C6', 'D6']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'D9', 'D9']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'ST', 'DT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'ST', 'CT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'ST', 'HT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'HT', 'DT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'HT', 'CT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'CT', 'DT']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'SJ', 'DJ']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'CQ', 'CQ']], ['ThreeWithTwo', 'A', ['CA', 'CA', 'H2', 'S2', 'C2']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'H4', 'C4']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'S6', 'D6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'S6', 'C6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'S6', 'H6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'H6', 'D6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'H6', 'C6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'C6', 'D6']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'D9', 'D9']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'ST', 'DT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'ST', 'CT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'ST', 'HT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'HT', 'DT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'HT', 'CT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'CT', 'DT']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'SJ', 'DJ']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'CQ', 'CQ']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'SA', 'CA']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'SA', 'HA']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'HA', 'CA']], ['ThreeWithTwo', '2', ['S2', 'H2', 'C2', 'CA', 'CA']], ['TwoTrips', 'A', ['SA', 'HA', 'CA', 'S2', 'H2', 'C2']], ['TwoTrips', 'A', ['SA', 'CA', 'CA', 'S2', 'H2', 'C2']], ['TwoTrips', 'A', ['HA', 'CA', 'CA', 'S2', 'H2', 'C2']], ['TwoTrips', '9', ['D9', 'D9', 'H2', 'ST', 'HT', 'DT']], ['TwoTrips', '9', ['D9', 'D9', 'H2', 'ST', 'HT', 'CT']], ['TwoTrips', '9', ['D9', 'D9', 'H2', 'ST', 'CT', 'DT']], ['TwoTrips', '9', ['D9', 'D9', 'H2', 'HT', 'CT', 'DT']], ['TwoTrips', 'T', ['ST', 'HT', 'DT', 'SJ', 'DJ', 'H2']], ['TwoTrips', 'T', ['ST', 'HT', 'CT', 'SJ', 'DJ', 'H2']], ['TwoTrips', 'T', ['ST', 'CT', 'DT', 'SJ', 'DJ', 'H2']], ['TwoTrips', 'T', ['HT', 'CT', 'DT', 'SJ', 'DJ', 'H2']], ['Straight', 'A', ['SA', 'S2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['SA', 'S2', 'H2', 'C4', 'D5']], ['Straight', 'A', ['SA', 'C2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['SA', 'C2', 'H2', 'C4', 'D5']], ['Straight', 'A', ['HA', 'S2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['HA', 'S2', 'H2', 'C4', 'D5']], ['Straight', 'A', ['HA', 'C2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['HA', 'C2', 'H2', 'C4', 'D5']], ['Straight', 'A', ['CA', 'S2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['CA', 'S2', 'H2', 'C4', 'D5']], ['Straight', 'A', ['CA', 'C2', 'H2', 'H4', 'D5']], ['Straight', 'A', ['CA', 'C2', 'H2', 'C4', 'D5']], ['Straight', '2', ['S2', 'H2', 'H4', 'D5', 'S6']], ['Straight', '2', ['S2', 'H2', 'H4', 'D5', 'H6']], ['Straight', '2', ['S2', 'H2', 'H4', 'D5', 'C6']], ['Straight', '2', ['S2', 'H2', 'H4', 'D5', 'D6']], ['Straight', '2', ['S2', 'H2', 'C4', 'D5', 'S6']], ['Straight', '2', ['S2', 'H2', 'C4', 'D5', 'H6']], ['Straight', '2', ['S2', 'H2', 'C4', 'D5', 'C6']], ['Straight', '2', ['S2', 'H2', 'C4', 'D5', 'D6']], ['Straight', '2', ['C2', 'H2', 'H4', 'D5', 'S6']], ['Straight', '2', ['C2', 'H2', 'H4', 'D5', 'H6']], ['Straight', '2', ['C2', 'H2', 'H4', 'D5', 'C6']], ['Straight', '2', ['C2', 'H2', 'H4', 'D5', 'D6']], ['Straight', '2', ['C2', 'H2', 'C4', 'D5', 'S6']], ['Straight', '2', ['C2', 'H2', 'C4', 'D5', 'H6']], ['Straight', '2', ['C2', 'H2', 'C4', 'D5', 'C6']], ['Straight', '2', ['C2', 'H2', 'C4', 'D5', 'D6']], ['Straight', '3', ['H2', 'H4', 'D5', 'S6', 'H7']], ['Straight', '3', ['H2', 'H4', 'D5', 'H6', 'H7']], ['Straight', '3', ['H2', 'H4', 'D5', 'C6', 'H7']], ['Straight', '3', ['H2', 'H4', 'D5', 'D6', 'H7']], ['Straight', '3', ['H2', 'C4', 'D5', 'S6', 'H7']], ['Straight', '3', ['H2', 'C4', 'D5', 'H6', 'H7']], ['Straight', '3', ['H2', 'C4', 'D5', 'C6', 'H7']], ['Straight', '3', ['H2', 'C4', 'D5', 'D6', 'H7']], ['Straight', '4', ['H4', 'D5', 'S6', 'H7', 'D8']], ['Straight', '4', ['H4', 'D5', 'S6', 'H7', 'H2']], ['Straight', '4', ['H4', 'D5', 'S6', 'H2', 'D8']], ['Straight', '4', ['H4', 'D5', 'H6', 'H7', 'D8']], ['Straight', '4', ['H4', 'D5', 'H6', 'H7', 'H2']], ['Straight', '4', ['H4', 'D5', 'H6', 'H2', 'D8']], ['Straight', '4', ['H4', 'D5', 'C6', 'H7', 'D8']], ['Straight', '4', ['H4', 'D5', 'C6', 'H7', 'H2']], ['Straight', '4', ['H4', 'D5', 'C6', 'H2', 'D8']], ['Straight', '4', ['H4', 'D5', 'D6', 'H7', 'D8']], ['Straight', '4', ['H4', 'D5', 'D6', 'H7', 'H2']], ['Straight', '4', ['H4', 'D5', 'D6', 'H2', 'D8']], ['Straight', '4', ['H4', 'D5', 'H2', 'H7', 'D8']], ['Straight', '4', ['H4', 'H2', 'S6', 'H7', 'D8']], ['Straight', '4', ['H4', 'H2', 'H6', 'H7', 'D8']], ['Straight', '4', ['H4', 'H2', 'C6', 'H7', 'D8']], ['Straight', '4', ['H4', 'H2', 'D6', 'H7', 'D8']], ['Straight', '4', ['C4', 'D5', 'S6', 'H7', 'D8']], ['Straight', '4', ['C4', 'D5', 'S6', 'H7', 'H2']], ['Straight', '4', ['C4', 'D5', 'S6', 'H2', 'D8']], ['Straight', '4', ['C4', 'D5', 'H6', 'H7', 'D8']], ['Straight', '4', ['C4', 'D5', 'H6', 'H7', 'H2']], ['Straight', '4', ['C4', 'D5', 'H6', 'H2', 'D8']], ['Straight', '4', ['C4', 'D5', 'C6', 'H7', 'D8']], ['Straight', '4', ['C4', 'D5', 'C6', 'H7', 'H2']], ['Straight', '4', ['C4', 'D5', 'C6', 'H2', 'D8']], ['Straight', '4', ['C4', 'D5', 'D6', 'H7', 'D8']], ['Straight', '4', ['C4', 'D5', 'D6', 'H7', 'H2']], ['Straight', '4', ['C4', 'D5', 'D6', 'H2', 'D8']], ['Straight', '4', ['C4', 'D5', 'H2', 'H7', 'D8']], ['Straight', '4', ['C4', 'H2', 'S6', 'H7', 'D8']], ['Straight', '4', ['C4', 'H2', 'H6', 'H7', 'D8']], ['Straight', '4', ['C4', 'H2', 'C6', 'H7', 'D8']], ['Straight', '4', ['C4', 'H2', 'D6', 'H7', 'D8']], ['Straight', '4', ['H2', 'D5', 'S6', 'H7', 'D8']], ['Straight', '4', ['H2', 'D5', 'H6', 'H7', 'D8']], ['Straight', '4', ['H2', 'D5', 'C6', 'H7', 'D8']], ['Straight', '4', ['H2', 'D5', 'D6', 'H7', 'D8']], ['Straight', '5', ['D5', 'S6', 'H7', 'D8', 'D9']], ['Straight', '5', ['D5', 'S6', 'H7', 'D8', 'H2']], ['Straight', '5', ['D5', 'S6', 'H7', 'H2', 'D9']], ['Straight', '5', ['D5', 'S6', 'H2', 'D8', 'D9']], ['Straight', '5', ['D5', 'H6', 'H7', 'D8', 'D9']], ['Straight', '5', ['D5', 'H6', 'H7', 'D8', 'H2']], ['Straight', '5', ['D5', 'H6', 'H7', 'H2', 'D9']], ['Straight', '5', ['D5', 'H6', 'H2', 'D8', 'D9']], ['Straight', '5', ['D5', 'C6', 'H7', 'D8', 'D9']], ['Straight', '5', ['D5', 'C6', 'H7', 'D8', 'H2']], ['Straight', '5', ['D5', 'C6', 'H7', 'H2', 'D9']], ['Straight', '5', ['D5', 'C6', 'H2', 'D8', 'D9']], ['Straight', '5', ['D5', 'D6', 'H7', 'D8', 'D9']], ['Straight', '5', ['D5', 'D6', 'H7', 'D8', 'H2']], ['Straight', '5', ['D5', 'D6', 'H7', 'H2', 'D9']], ['Straight', '5', ['D5', 'D6', 'H2', 'D8', 'D9']], ['Straight', '5', ['D5', 'H2', 'H7', 'D8', 'D9']], ['Straight', '5', ['H2', 'S6', 'H7', 'D8', 'D9']], ['Straight', '5', ['H2', 'H6', 'H7', 'D8', 'D9']], ['Straight', '5', ['H2', 'C6', 'H7', 'D8', 'D9']], ['Straight', '5', ['H2', 'D6', 'H7', 'D8', 'D9']], ['Straight', '6', ['S6', 'H7', 'D8', 'D9', 'ST']], ['Straight', '6', ['S6', 'H7', 'D8', 'D9', 'HT']], ['Straight', '6', ['S6', 'H7', 'D8', 'D9', 'CT']], ['Straight', '6', ['S6', 'H7', 'D8', 'D9', 'DT']], ['Straight', '6', ['S6', 'H7', 'D8', 'D9', 'H2']], ['Straight', '6', ['S6', 'H7', 'D8', 'H2', 'ST']], ['Straight', '6', ['S6', 'H7', 'D8', 'H2', 'HT']], ['Straight', '6', ['S6', 'H7', 'D8', 'H2', 'CT']], ['Straight', '6', ['S6', 'H7', 'D8', 'H2', 'DT']], ['Straight', '6', ['S6', 'H7', 'H2', 'D9', 'ST']], ['Straight', '6', ['S6', 'H7', 'H2', 'D9', 'HT']], ['Straight', '6', ['S6', 'H7', 'H2', 'D9', 'CT']], ['Straight', '6', ['S6', 'H7', 'H2', 'D9', 'DT']], ['Straight', '6', ['S6', 'H2', 'D8', 'D9', 'ST']], ['Straight', '6', ['S6', 'H2', 'D8', 'D9', 'HT']], ['Straight', '6', ['S6', 'H2', 'D8', 'D9', 'CT']], ['Straight', '6', ['S6', 'H2', 'D8', 'D9', 'DT']], ['Straight', '6', ['H6', 'H7', 'D8', 'D9', 'ST']], ['Straight', '6', ['H6', 'H7', 'D8', 'D9', 'HT']], ['Straight', '6', ['H6', 'H7', 'D8', 'D9', 'CT']], ['Straight', '6', ['H6', 'H7', 'D8', 'D9', 'DT']], ['Straight', '6', ['H6', 'H7', 'D8', 'D9', 'H2']], ['Straight', '6', ['H6', 'H7', 'D8', 'H2', 'ST']], ['Straight', '6', ['H6', 'H7', 'D8', 'H2', 'HT']], ['Straight', '6', ['H6', 'H7', 'D8', 'H2', 'CT']], ['Straight', '6', ['H6', 'H7', 'D8', 'H2', 'DT']], ['Straight', '6', ['H6', 'H7', 'H2', 'D9', 'ST']], ['Straight', '6', ['H6', 'H7', 'H2', 'D9', 'HT']], ['Straight', '6', ['H6', 'H7', 'H2', 'D9', 'CT']], ['Straight', '6', ['H6', 'H7', 'H2', 'D9', 'DT']], ['Straight', '6', ['H6', 'H2', 'D8', 'D9', 'ST']], ['Straight', '6', ['H6', 'H2', 'D8', 'D9', 'HT']], ['Straight', '6', ['H6', 'H2', 'D8', 'D9', 'CT']], ['Straight', '6', ['H6', 'H2', 'D8', 'D9', 'DT']], ['Straight', '6', ['C6', 'H7', 'D8', 'D9', 'ST']], ['Straight', '6', ['C6', 'H7', 'D8', 'D9', 'HT']], ['Straight', '6', ['C6', 'H7', 'D8', 'D9', 'CT']], ['Straight', '6', ['C6', 'H7', 'D8', 'D9', 'DT']], ['Straight', '6', ['C6', 'H7', 'D8', 'D9', 'H2']], ['Straight', '6', ['C6', 'H7', 'D8', 'H2', 'ST']], ['Straight', '6', ['C6', 'H7', 'D8', 'H2', 'HT']], ['Straight', '6', ['C6', 'H7', 'D8', 'H2', 'CT']], ['Straight', '6', ['C6', 'H7', 'D8', 'H2', 'DT']], ['Straight', '6', ['C6', 'H7', 'H2', 'D9', 'ST']], ['Straight', '6', ['C6', 'H7', 'H2', 'D9', 'HT']], ['Straight', '6', ['C6', 'H7', 'H2', 'D9', 'CT']], ['Straight', '6', ['C6', 'H7', 'H2', 'D9', 'DT']], ['Straight', '6', ['C6', 'H2', 'D8', 'D9', 'ST']], ['Straight', '6', ['C6', 'H2', 'D8', 'D9', 'HT']], ['Straight', '6', ['C6', 'H2', 'D8', 'D9', 'CT']], ['Straight', '6', ['C6', 'H2', 'D8', 'D9', 'DT']], ['Straight', '6', ['D6', 'H7', 'D8', 'D9', 'ST']], ['Straight', '6', ['D6', 'H7', 'D8', 'D9', 'HT']], ['Straight', '6', ['D6', 'H7', 'D8', 'D9', 'CT']], ['Straight', '6', ['D6', 'H7', 'D8', 'D9', 'DT']], ['Straight', '6', ['D6', 'H7', 'D8', 'D9', 'H2']], ['Straight', '6', ['D6', 'H7', 'D8', 'H2', 'ST']], ['Straight', '6', ['D6', 'H7', 'D8', 'H2', 'HT']], ['Straight', '6', ['D6', 'H7', 'D8', 'H2', 'CT']], ['Straight', '6', ['D6', 'H7', 'D8', 'H2', 'DT']], ['Straight', '6', ['D6', 'H7', 'H2', 'D9', 'ST']], ['Straight', '6', ['D6', 'H7', 'H2', 'D9', 'HT']], ['Straight', '6', ['D6', 'H7', 'H2', 'D9', 'CT']], ['Straight', '6', ['D6', 'H7', 'H2', 'D9', 'DT']], ['Straight', '6', ['D6', 'H2', 'D8', 'D9', 'ST']], ['Straight', '6', ['D6', 'H2', 'D8', 'D9', 'HT']], ['Straight', '6', ['D6', 'H2', 'D8', 'D9', 'CT']], ['Straight', '6', ['D6', 'H2', 'D8', 'D9', 'DT']], ['Straight', '6', ['H2', 'H7', 'D8', 'D9', 'ST']], ['Straight', '6', ['H2', 'H7', 'D8', 'D9', 'HT']], ['Straight', '6', ['H2', 'H7', 'D8', 'D9', 'CT']], ['Straight', '6', ['H2', 'H7', 'D8', 'D9', 'DT']], ['Straight', '7', ['H7', 'D8', 'D9', 'ST', 'SJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'ST', 'DJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'ST', 'H2']], ['Straight', '7', ['H7', 'D8', 'D9', 'HT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'HT', 'DJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'HT', 'H2']], ['Straight', '7', ['H7', 'D8', 'D9', 'CT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'CT', 'DJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'CT', 'H2']], ['Straight', '7', ['H7', 'D8', 'D9', 'DT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'DT', 'DJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'DT', 'H2']], ['Straight', '7', ['H7', 'D8', 'D9', 'H2', 'SJ']], ['Straight', '7', ['H7', 'D8', 'D9', 'H2', 'DJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'ST', 'SJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'ST', 'DJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'HT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'HT', 'DJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'CT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'CT', 'DJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'DT', 'SJ']], ['Straight', '7', ['H7', 'D8', 'H2', 'DT', 'DJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'ST', 'SJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'ST', 'DJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'HT', 'SJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'HT', 'DJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'CT', 'SJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'CT', 'DJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'DT', 'SJ']], ['Straight', '7', ['H7', 'H2', 'D9', 'DT', 'DJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'ST', 'SJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'ST', 'DJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'HT', 'SJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'HT', 'DJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'CT', 'SJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'CT', 'DJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'DT', 'SJ']], ['Straight', '7', ['H2', 'D8', 'D9', 'DT', 'DJ']], ['Straight', '8', ['D8', 'D9', 'ST', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'ST', 'SJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'ST', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'ST', 'DJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'ST', 'H2', 'CQ']], ['Straight', '8', ['D8', 'D9', 'HT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'HT', 'SJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'HT', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'HT', 'DJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'HT', 'H2', 'CQ']], ['Straight', '8', ['D8', 'D9', 'CT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'CT', 'SJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'CT', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'CT', 'DJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'CT', 'H2', 'CQ']], ['Straight', '8', ['D8', 'D9', 'DT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'DT', 'SJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'DT', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'DT', 'DJ', 'H2']], ['Straight', '8', ['D8', 'D9', 'DT', 'H2', 'CQ']], ['Straight', '8', ['D8', 'D9', 'H2', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'D9', 'H2', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'ST', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'ST', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'HT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'HT', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'CT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'CT', 'DJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'DT', 'SJ', 'CQ']], ['Straight', '8', ['D8', 'H2', 'DT', 'DJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'ST', 'SJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'ST', 'DJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'HT', 'SJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'HT', 'DJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'CT', 'SJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'CT', 'DJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'DT', 'SJ', 'CQ']], ['Straight', '8', ['H2', 'D9', 'DT', 'DJ', 'CQ']], ['Straight', '9', ['D9', 'ST', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'ST', 'SJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'ST', 'SJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'ST', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'ST', 'DJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'ST', 'DJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'ST', 'H2', 'CQ', 'CK']], ['Straight', '9', ['D9', 'HT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'HT', 'SJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'HT', 'SJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'HT', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'HT', 'DJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'HT', 'DJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'HT', 'H2', 'CQ', 'CK']], ['Straight', '9', ['D9', 'CT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'CT', 'SJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'CT', 'SJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'CT', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'CT', 'DJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'CT', 'DJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'CT', 'H2', 'CQ', 'CK']], ['Straight', '9', ['D9', 'DT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'DT', 'SJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'DT', 'SJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'DT', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'DT', 'DJ', 'CQ', 'H2']], ['Straight', '9', ['D9', 'DT', 'DJ', 'H2', 'CK']], ['Straight', '9', ['D9', 'DT', 'H2', 'CQ', 'CK']], ['Straight', '9', ['D9', 'H2', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['D9', 'H2', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'ST', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'ST', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'HT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'HT', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'CT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'CT', 'DJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'DT', 'SJ', 'CQ', 'CK']], ['Straight', '9', ['H2', 'DT', 'DJ', 'CQ', 'CK']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['ST', 'SJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['ST', 'SJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['ST', 'SJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['ST', 'SJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['ST', 'DJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['ST', 'DJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['ST', 'DJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['ST', 'DJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['ST', 'H2', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['ST', 'H2', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['ST', 'H2', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['HT', 'SJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['HT', 'SJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['HT', 'SJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['HT', 'SJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['HT', 'DJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['HT', 'DJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['HT', 'DJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['HT', 'DJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['HT', 'H2', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['HT', 'H2', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['HT', 'H2', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['CT', 'SJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['CT', 'SJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['CT', 'SJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['CT', 'SJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['CT', 'DJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['CT', 'DJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['CT', 'DJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['CT', 'DJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['CT', 'H2', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['CT', 'H2', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['CT', 'H2', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['DT', 'SJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['DT', 'SJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['DT', 'SJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['DT', 'SJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'CK', 'H2']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'H2', 'SA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'H2', 'HA']], ['Straight', 'T', ['DT', 'DJ', 'CQ', 'H2', 'CA']], ['Straight', 'T', ['DT', 'DJ', 'H2', 'CK', 'SA']], ['Straight', 'T', ['DT', 'DJ', 'H2', 'CK', 'HA']], ['Straight', 'T', ['DT', 'DJ', 'H2', 'CK', 'CA']], ['Straight', 'T', ['DT', 'H2', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['DT', 'H2', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['DT', 'H2', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['H2', 'SJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['H2', 'SJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['H2', 'SJ', 'CQ', 'CK', 'CA']], ['Straight', 'T', ['H2', 'DJ', 'CQ', 'CK', 'SA']], ['Straight', 'T', ['H2', 'DJ', 'CQ', 'CK', 'HA']], ['Straight', 'T', ['H2', 'DJ', 'CQ', 'CK', 'CA']], ['Bomb', '6', ['S6', 'H6', 'C6', 'H2']], ['Bomb', '6', ['S6', 'H6', 'C6', 'D6']], ['Bomb', '6', ['S6', 'H6', 'D6', 'H2']], ['Bomb', '6', ['S6', 'C6', 'D6', 'H2']], ['Bomb', '6', ['H6', 'C6', 'D6', 'H2']], ['Bomb', 'T', ['ST', 'HT', 'CT', 'H2']], ['Bomb', 'T', ['ST', 'HT', 'CT', 'DT']], ['Bomb', 'T', ['ST', 'HT', 'DT', 'H2']], ['Bomb', 'T', ['ST', 'CT', 'DT', 'H2']], ['Bomb', 'T', ['HT', 'CT', 'DT', 'H2']], ['Bomb', 'A', ['SA', 'HA', 'CA', 'H2']], ['Bomb', 'A', ['SA', 'HA', 'CA', 'CA']], ['Bomb', 'A', ['SA', 'CA', 'CA', 'H2']], ['Bomb', 'A', ['HA', 'CA', 'CA', 'H2']], ['Bomb', '6', ['S6', 'H6', 'C6', 'D6', 'H2']], ['Bomb', 'T', ['ST', 'HT', 'CT', 'DT', 'H2']], ['Bomb', 'A', ['SA', 'HA', 'CA', 'CA', 'H2']]], 'indexRange': 1310}
# # act=msg['actionList']
# gp=msg['greaterPos']
# act=data['actionList']
# print(msg['curPos'])
# print(lasthand.firstcard(hd,'2')[0])
# print(lasthand.firstcard(hd,'2')[1])
# print("二手配完牌",lasthand.lgetcard(lasthand.firstcard(hd,'2')[0],lasthand.firstcard(hd,'2')[1]))
# # print("寻找索引",lasthand.getindex(act,lasthand.getcolor(lasthand.lgetcard(lasthand.firstcard(hd,'2')[0],lasthand.firstcard(hd,'2')[1]),'2')))
# print("这是手牌",lasthand.lgetcard(lasthand.firstcard(hd,'2')[0],lasthand.firstcard(hd,'2')[1]))
# print("index",lasthand.getindex(act,lasthand.getcolor(lasthand.lgetcard(lasthand.firstcard(hd,msg['curRank'])[0],lasthand.firstcard(hd,msg['curRank'])[1]),'2')))
# print("这是要出的牌",lasthand.getcolor(lasthand.lgetcard(lasthand.firstcard(hd,msg['curRank'])[0],lasthand.firstcard(hd,msg['curRank'])[1]),'2'))
# print("拿到索引",lasthand.getindex(act,['S3', 'C3']))

