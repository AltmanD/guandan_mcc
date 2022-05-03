class lasthand(object):


    def firstcard(self, hd, cur):
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R']
        poke.remove(cur)
        poke.insert(12,cur)
        hdcopy = hd[:]
        num = 0
        dict = {'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [],
                'ThreeWithTwo': [], 'TwoTrips': [], 'Straight': [], 'Bomb': [], 'StraightFlush': [], 'numh': []}
        # 寻找红桃配
        for i in hdcopy:
            # print(i)
            if i.find(cur) == 1 and i[0] == 'H':
                dict['numh'].append(i)
        # print(len(self.getcard(hdcopy, dict['numh'])['Straight'][1]))
        while len(self.getcard(hdcopy, dict['numh'])['Straight']) > 0:
            # print("长度",len(getcard(hdcopy))['Straight'][1::2])
            # print("getcard的顺子", self.getcard(hdcopy, dict['numh'])['Straight'])
            dict['Straight'].append(self.getcard(hdcopy, dict['numh'])['Straight'][0][1])
            dict['Straight'].append(self.getcard(hdcopy, dict['numh'])['Straight'])
            for i in self.getcard(hdcopy, dict['numh'])['Straight']:
                hdcopy.remove(i)
                if dict['numh'].count(i) > 0:
                    dict['numh'].remove(i)
        dict['Bomb'] = self.getcard(hdcopy, dict['numh'])['Bomb']
        #print("这是Bomb", dict['Bomb'])
        if len(dict['Bomb']) > 0:
            for i in dict['Bomb'][1::2]:
                for j in i:
                    if poke.index(j[1]) <= 12:
                        hdcopy.remove(j)
        dict['TwoTrips'] = self.getcard(hdcopy, dict['numh'])['TwoTrips']
        print("???????",hdcopy,dict['TwoTrips'],self.getcard(hdcopy, dict['numh']))
        if len(dict['TwoTrips']) > 0:
             for i in dict['TwoTrips'][1::2]:
                for j in i:
                    if poke.index(j[1]) <=8:
                        hdcopy.remove(j)
        dict['ThreePair'] = self.getcard(hdcopy, dict['numh'])['ThreePair']
        if len(dict['ThreePair']) > 0:
            for i in dict['ThreePair'][1::2]:
                for j in i:
                    if poke.index(j[1]) <=10:
                        hdcopy.remove(j)
        dict['Single']=[]
        dict['Pair']=[]
        dict['Trips']=[]
        # print("这是hdcopy", hdcopy)
        print("这是先手配的牌",dict)
        return (hdcopy, dict)

    def getcard(self, hd, numh):
        poke = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'B', 'R']
        pn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dict = {'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [],
                'ThreeWithTwo': [], 'TwoTrips': [], 'Straight': [], 'Bomb': [], 'StraightFlush': [], 'numh': [],'boom':[]}
        lnumh = len(numh)
        # print("有", lnumh, "个红桃配")
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
            elif len(colorlist) == 3 and lnumh > 0 and i != numh[0][1]:
                lnumh -= 1
                # print(lnumh)
                # print(colorlist)
                dict['Bomb'].append(i)
                colorlist.append(numh[0])
                dict['Bomb'].append(colorlist)
            elif len(colorlist) == 3:
                dict['Trips'].append(i)
                dict['Trips'].append(colorlist)
            elif len(colorlist) >= 4:
                dict['boom'].append(i)
                dict['boom'].append(colorlist)
            # elif len(colorlist)>=4:
        #    dict['Bomb'].append(i)
        #   dict['Bomb'].append(colorlist)
        # 寻找三带二
        # 配顺子
        # 寻找连对
        # 寻找顺子
        # print(dict['Straight'])
        dict['Straight'] = self.lgetsunzi(dict)
        dict['ThreePair'] += self.getliandui(dict)
        #print("这是dict1",self.lgetttr(dict))
        dict['TwoTrips']+=self.lgetttr(dict)
        #print("这是钢板",dict['TwoTrips'],dict)
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
        poke = ['A','2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q','K']
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
        print("这是配钢板")
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T']
        #print(dict['Trips'][::2])
        trip = dict['Trips'][::2]
        print("这是trip",trip)
        ez = []
        cldui = []
        dui = []
        num = 0
        for i in poke:
            if trip.count(i) == 1:
                ez.append(i)
                if len(ez) >= 2:
                    print(ez)
                    for i in ez:
                       # print(dict['Trips'][dict['Trips'].index(i) + 1][0])
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
        print("这是钢板", dui)
        return dui

    def hgetcard(self,hd,dict,cur):
        poke = [ '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K','A', 'B', 'R']
        leng=0
        poke.remove(cur)
        poke.insert(12,cur)
        for i in dict["Single"][::2]:
            if poke.index(i)<=12:
                leng+=1
        print("这是单张的长度",leng,len(dict["Single"][::2]))
        leng-=len(dict["Single"][::2])-leng
        print("小于A的单张的长度",leng,poke[11])
        pn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
            elif len(colorlist) == 1 :
                    dict['Single'].append(i)
                    dict['Single'].append(colorlist)
            elif len(colorlist) == 2 :
                dict['Pair'].append(i)
                dict['Pair'].append(colorlist)
            elif len(colorlist) == 3:
                dict['Trips'].append(i)
                dict['Trips'].append(colorlist)
            elif len(colorlist) >= 4:
                dict['Bomb'].append(i)
                dict['Bomb'].append(colorlist)

        # 寻找三带二
        if len(dict['Trips']) > 0 and len(dict['Pair']) > 0:
            for i in dict['Trips'][::2]:
                dict['ThreeWithTwo'].append(i)
                twt = dict['Trips'][dict['Trips'].index(i) + 1] + dict['Pair'][1]
                dict['ThreeWithTwo'].append(twt)
        #把当前最大的牌放到顺子和单张里面
        #配顺子
        dict['Straight'] += self.getsunzi(dict)
        # 寻找连对
        dict['ThreePair'] += self.getliandui(dict)
        dict['TwoTrips'] +=self.lgetttr(dict)
        # 寻找顺子
        # 拆牌出
        for i in dict['Pair'][::2]:
            if poke.index(i)>=11:
                si=[]
                si.append(dict['Pair'][dict['Pair'].index(i) + 1][0])
                dict['Single'].append(i)
                dict['Single'].append(si)
        for i in dict['Bomb'][::2]:
            if poke.index(i)>=11:
                si=[]
                si.append(dict['Bomb'][dict['Bomb'].index(i) + 1][0])
                dict['Single'].append(i)
                dict['Single'].append(si)
        for i in dict['Trips'][::2]:
            if poke.index(i)>=11:
                si=[]
                si.append(dict['Trips'][dict['Trips'].index(i) + 1][0])
                dict['Single'].append(i)
                dict['Single'].append(si)
        for i in dict['Bomb'][::2]:
            if poke.index(i)>=11:
                dict['Pair'].append(i)
                dict['Pair'].append(dict['Bomb'][dict['Bomb'].index(i) + 1][:2])
        for i in dict['Trips'][::2]:
            if poke.index(i)>=11:
                dict['Pair'].append(i)
                dict['Pair'].append(dict['Trips'][dict['Trips'].index(i) + 1][:2])
        return dict

    def getsunzi(self, dict):
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
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
                        if num > -1:
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
        poke = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'B', 'R']
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
                    if num >1:
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

    def getcolor(self,dict,cur,greaterPos):
        index=[]
        #判断小于A的单张的长度
#        print("这是single",len(dict["Single"]))
        leng=0
        min=99
        poker=['2','3','4','5','6','7','8','9','T','J','Q','K','A','B','R','JOKER']
        poker.remove(cur)
        poker.insert(12,cur)
        # 判断小于A的单张的长度
        for i in dict["Single"][::2]:
            if poker.index(i)<=12:
                leng+=1
        print("这是单张的长度",leng,len(dict["Single"][::2]))
        leng-=len(dict["Single"][::2])-leng
        print("小于A的单张的长度",leng,poker[11])
        # print(poker)
        for i in dict[greaterPos[0]][::2]:
            #eval(play_data['greaterAction'])[0]
            #print("这是要要出的牌的类型",dict[greaterPos[0]])
            # print(poker.index(i),poker.index(greaterPos[1]))
            if poker.index(i)>poker.index(greaterPos[1]) and poker.index(i)<min:
              if leng>=2 and poker.index(i)>=12:
                  index=[]
              else:
                  index=dict[greaterPos[0]][dict[greaterPos[0]].index(i)+1]
                  min=poker.index(i)
                # print(min)
                # print(index)
        return index
    def getindex(self,actionlist,color):
        index=0
        for i in actionlist:
            if color==i[2]:
                index=actionlist.index(i)
        return  index

    def getBomb(self,greatpos, dict, cur):
        poker = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'B', 'R','JOKER']
        print("这是Bomb",dict)
        poker.remove(cur)
        poker.insert(12, cur)
        msg = []
        bom = dict['Bomb']
        if greatpos[0] != 'Bomb' and greatpos[0] != 'StraightFlush' and len(bom) != 0:
            msg = bom[1]
            # print(msg)
        elif greatpos[0] == 'Bomb':
            for i in bom[::2]:
                # 此处可优化 ，
                if poker.index(i) > poker.index(greatpos[1]) and len(bom[bom.index(i) + 1]) == len(greatpos[2]):
                    msg = bom[bom.index(i) + 1]
                elif len(bom[bom.index(i) + 1]) > len(greatpos[2]):
                    msg = bom[bom.index(i) + 1]
        elif greatpos[0] == 'StraightFlush':
            for i in bom[1::2]:
                if len(i) > 5:
                    msg = i
        return msg
    def getlen(self,dict):
        # dict = {'Single': [], 'Pair': [], 'Trips': [], 'ThreePair': [],
        #         'ThreeWithTwo': [], 'ThreePair': [], 'Straight': [], 'Bomb': [], 'StraightFlush': []}
        num=0
        numb=len(dict['Bomb'])
        if len(dict['ThreeWithTwo'])==0:
            num=len(dict['Single'])+len(dict['Pair'])+len(dict['Trips'])
        else:
            num =len(dict['Single'])+len(dict['ThreeWithTwo'])+(len(dict['Pair'])-len(dict['ThreeWithTwo']))+(len(dict['Trips'])-len(dict['ThreeWithTwo']))
        if numb >= num:
            return 1
        else:
            return 0

    def client_xia(self,num):
        client_num = [0, 1, 2, 3]
        if num == 3:
            num = 0
            return client_num[num]
        else:
            return client_num[num + 1]

    def client_shang(self,num):
        client_num = [0, 1, 2, 3]
        if num == 0:
            num = 3
            return client_num[num]
        else:
            return client_num[num - 1]


# lasthand=lasthand()
# data={"type": "notify","stage": "beginning","handCards": ['H2', 'H2', 'C4', 'H5', 'H5', 'D5', 'D6', 'S7', 'S7', 'C7', 'C7', 'D7', 'S8', 'S8', 'C8', 'H9', 'CT', 'DT', 'SQ', 'CQ', 'DQ', 'DK', 'DA', 'HJ', 'CJ', 'DJ', 'SB']}
# hd=data['handCards']
# lh=lasthand
# msg={'type': 'act',
#  'handCards': ['H2', 'H2', 'C4', 'H5', 'H5', 'D5', 'D6', 'S7', 'S7', 'C7', 'C7', 'D7', 'S8', 'S8', 'C8', 'H9', 'CT', 'DT', 'HJ', 'CJ', 'DJ','SQ', 'CQ', 'DQ', 'DK', 'DA', 'SB'],
#  'publicInfo': [{'rest': 22,
#    'playArea': ['ThreeWithTwo', 'A', ['SA', 'SA', 'DA', 'H8', 'D8']]},
#   {'rest': 23, 'playArea': ['Bomb', '4', ['H4', 'H4', 'C4', 'D4']]},
#   {'rest': 23, 'playArea': ['Bomb', 'A', ['HA', 'HA', 'CA', 'DA']]},
#   {'rest': 27, 'playArea': None}],
#  'selfRank': 'K',
#  'oppoRank': '9',
#  'curRank': '9',
#  'stage': 'play',
#  'curPos': 2,
#  'curAction': ['Bomb', 'A', ['HA', 'HA', 'CA', 'DA']],
#  'greaterAction': 2,
#  'greaterPos': ['Bomb', 'A', ['HA', 'HA', 'CA', 'DA']],
#  'actionList': [['PASS', 'PASS', 'PASS'],
#   ['Bomb', '9', ['H9', 'H9', 'C9', 'D9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'C2', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'C2', 'D2']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'D2', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'C2', 'D2', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'C2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'C2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['H2', 'H2', 'C2', 'D2', 'H9']],
#   ['Bomb', '2', ['H2', 'H2', 'C2', 'H9', 'H9']],
#   ['Bomb', '2', ['H2', 'H2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['H2', 'C2', 'D2', 'H9', 'H9']],
#   ['Bomb', '3', ['S3', 'H3', 'D3', 'H9', 'H9']],
#   ['Bomb', 'Q', ['HQ', 'HQ', 'CQ', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'C2', 'D2', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'C2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'C2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['H2', 'H2', 'C2', 'D2', 'H9', 'H9']],
#   ['Bomb', '2', ['S2', 'H2', 'H2', 'C2', 'D2', 'H9', 'H9']]],
#  'indexRange': 21}
# act=msg['actionList']
# gp=msg['greaterPos']
# print("这是配牌",lasthand.firstcard(hd,'2')[0])
# print("这是后手配牌",lasthand.hgetcard(lasthand.firstcard(hd,'2')[0],lasthand.firstcard(hd,'2')[1],'2'))
# #print(lasthand.getcard(hd,'2'))
# print("index",lasthand.getindex(act,lasthand.getcolor(lasthand.hgetcard(lasthand.firstcard(hd,'2')[0],lasthand.firstcard(hd,'2')[1],'2'),'2',gp)))
# dict1 = lasthand.getcard(data['handCards'],['H2','H2'])
# print(lasthand.getindex(msg['actionList'],lasthand.getBomb(msg['greaterPos'], dict1,msg['curRank'])))
