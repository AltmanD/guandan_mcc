# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 19:21
# @Author     : Duofeng Wu
# @File       : gd_handle.py
# @Description: 自动解析掼蛋所发送来的JSON数据

class State(object):

    def __init__(self,name):

        """
        每个实例的保护属性对应JSON中的字段值，私有属性表示根据不同type和stage进行不同解析。
        type:          表示消息类型。可取值包括notify和act。notify表示通知类型，act表示动作类型（即收到该类型的消息时需要做出动作）
        stage:         表示游戏阶段。可取值包括beginning, play, tribute, anti-tribute, back, episodeOver, gameOver
                        分别对应开始阶段、出牌阶段、进贡阶段、抗贡阶段、还贡阶段、结束阶段
        myPos:         表示自己的座位号
        publicInfo:    表示游戏中玩家公共信息
        actionList:    表示可行的动作列表
        curAction:     表示某玩家做出的动作
        curPos:        表示做出当前动作的玩家的座位号
        greaterPos:    表示最大动作的玩家的座位号
        greaterAction: 表示最大到你工作
        handCards:     表示手牌
        oppoRank:      表示对手等级
        curRank:       表示当前游戏在使用的等级None
        selfRank:      表示我方等级
        antiNum:       表示抗贡人数
        antiPos:       表示抗贡玩家（们）的 座位号
        result:        表示进贡或者还贡的结果
        order:         表示完牌的次序
        curTimes:      当前的对局次数
        settingTimes   设定的对局次数
        victoryNum     表示达到设定场次时的最终结果（哪一方赢得多）
        parse_func:    表示用于解析的函数
        """

        # history = {'0': {'send': [], 'remain': 27}, ...} 记录用户打出的牌
        # remain_cards = [4 * 14] 记录牌库剩余牌
        # played_cards = {'0': [], ...} 本轮用户打出的牌
        # player_id 用户id
        # current_hands = [] 当前手牌
        # action_list 可执行动作列表
        self.tribute_result = None
        self.history = {
            '0': {
                'send': [],
                'remain': 27,
            },
            '1': {
                'send': [],
                'remain': 27,
            },
            '2': {
                'send': [],
                'remain': 27,
            },
            '3': {
                'send': [],
                'remain': 27,
            },
        }
        self.remain_cards = {
            "S": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # s黑桃
            "H": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # h红桃
            "C": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # c方块
            "D": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # d梅花
        }
        self.play_cards = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
        }
        # 剩余牌的索引 1020
        self.remain_cards_classbynum = [8] * 13
        self.remain_cards_classbynum.append(2)
        self.remain_cards_classbynum.append(2)
        # end 1020

        self._type = None
        self._stage = None
        self._myPos = None
        self._publicInfo = None
        self._actionList = None
        self._curAction = None
        self._curPos = None
        self._greaterPos = None
        self._greaterAction = None
        self._handCards = None
        self._oppoRank = None
        self._curRank = None
        self._selfRank = None
        self._antiNum = None
        self._antiPos = None
        self._result = None
        self._order = None
        self._curTimes = None
        self._settingTimes = None
        self._victoryNum = None
        self._draws = None
        self._restCards = None
        self.pass_num = 0
        self.my_pass_num = 0

        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

        # TODO: 选手可根据(stage, type)自行定义处理的函数
        self.__parse_func = {
            ("beginning", "notify"): self.notify_begin,
            ("play", "notify"): self.notify_play,
            ("tribute", "notify"): self.notify_tribute,
            ("anti-tribute", "notify"): self.notify_anti,
            ("back", "notify"): self.notify_back,
            ("gameOver", "notify"): self.notify_game_over,
            ("episodeOver", "notify"): self.notify_episode_over,
            ("gameResult", "notify"): self.notify_game_result,

            ("play", "act"): self.act_play,
            ("tribute", "act"): self.act_tribute,
            ("back", "act"): self.act_back,
        }

    def parse(self, msg):
        assert type(msg) == dict
        for key, value in msg.items():
            setattr(self, "_{}".format(key), value)
        try:
            self.__parse_func[(self._stage, self._type)]()
            self._stage = None
            self._type = None
        except KeyError:
            print(msg)
            raise KeyError

    def notify_begin(self):
        """
        游戏开始阶段，告知每位玩家的手牌情况
        形如下所表示的JSON:
        {
            "type": "notify",
            "stage": "beginning",
            "handCard": ['S2', 'S2'],
            "myPos": 1,
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        print("游戏开始, 我是{}号位，手牌：{}".format(self._myPos, self._handCards))


    def notify_play(self):
        """
        出牌阶段，用于通知其他玩家做出了什么动作
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "play",
            "curPos": 1,
            "curAction": {"rank": '2', "type": Single, "actions": ['S2']},
            "greaterPos": 1,
            "greaterAction": {"rank": '2', "type": Single, "actions": ['S2']}
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        if self._curAction[2] != "PASS":
            for card in self._curAction[2]:
                card_type = str(card[0])
                self.history[str(self._curPos)]["send"].append(card)
                self.history[str(self._curPos)]["remain"] -= 1
                card_value = {"A": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10,
                              "Q": 11, "K": 12, "R": 13, "B": 13}
                x = card_value[card[1]]
                self.remain_cards[card_type][x] -= 1
        if self._curPos == (self._myPos+2)%4 or self._curPos == self._myPos:
            if self._curAction[0] == "PASS":
                self.pass_num += 1

            else:
                self.pass_num = 0

        if self._curPos == self._myPos:
            if self._curAction[0] == "PASS":
                self.my_pass_num += 1

            else:
                self.my_pass_num = 0


        # TODO: 选手可自行做出其他处理
        print("{}号位打出{}， 最大动作为{}号位打出的{}".format(self._curPos, self._curAction, self._greaterPos, self._greaterAction),"连续pass数目：", self.pass_num)


    def notify_tribute(self):
        """
        进贡阶段，用于通知所有玩家进贡者（们）都进贡了什么牌
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "tribute",
            "result": [[0, 3, 'S2']] 或 [[0, 3, 'S2'], [2, 1, 'S2']]
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        self.tribute_result = self._result
        for tribute_result in self._result:
            tribute_pos, receive_tribute_pos, card = tribute_result

            print("{}号位向{}号位进贡{}".format(tribute_pos, receive_tribute_pos, card))


    def notify_anti(self):
        """
        抗贡阶段，用于通知所有玩家，有人抗贡。其中antiNums的取值与antiPos数组的长度所对应
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "anti-tribute",
            "antiNums": 2,
            "antiPos": [0, 2]
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        for pos in self._antiPos:
            print("{}号位玩家抗贡".format(pos))

    def notify_back(self):
        """
        还贡阶段，用于通知所有玩家还贡者（们）都还贡了什么牌
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "back",
            "result": [[3, 0, 'S2']] 或 [[3, 0, 'S2'], [1, 2, 'S2']]
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        for back_result in self._result:
            back_pos, receive_back_pos, card = back_result
            print("{}号位向{}号位还贡{}".format(back_pos, receive_back_pos, card))

    def notify_episode_over(self):
        """
        小局结束阶段，用于通知所有玩家小局结束
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "episodeOver",
            "order": [0, 1, 2, 3]
            “curRank": 1,
            "restCards": [[pos, handcards], ...]
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # 重置字段
        self.history = {
            '0': {
                'send': [],
                'remain': 27,
            },
            '1': {
                'send': [],
                'remain': 27,
            },
            '2': {
                'send': [],
                'remain': 27,
            },
            '3': {
                'send': [],
                'remain': 27,
            },
        }
        self.remain_cards = {
            "S": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # s黑桃
            "H": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # h红桃
            "C": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # c方块
            "D": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # d梅花
        }
        self.play_cards = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
        }
        # 重置剩余牌的索引 1020
        self.remain_cards_classbynum = [8] * 13
        self.remain_cards_classbynum.append(2)
        self.remain_cards_classbynum.append(2)
        # end 1020
        self.pass_num = 0
        self.my_pass_num = 0
        # TODO: 选手可自行做出其他处理
        print("对局结束，完牌次序为{}，结束时所打的等级为{}".format(self._order, self._curRank))
        for rest in self._restCards:
            rest_pos, rest_cards = rest
            print("{}号位剩余卡牌{}".format(rest_pos, rest_cards))

    def notify_game_over(self):
        """
        到达指定游戏次数游戏结束，用于通知所有玩家游戏结束
        形如下所表示的JSON格式:
        {
            "type": "notify",
            "stage": "gameOver",
            "curTimes": 1
            “settingTimes": 1,
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # 重置字段
        self.history = {
            '0': {
                'send': [],
                'remain': 27,
            },
            '1': {
                'send': [],
                'remain': 27,
            },
            '2': {
                'send': [],
                'remain': 27,
            },
            '3': {
                'send': [],
                'remain': 27,
            },
        }
        self.remain_cards = {
            "S": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # s黑桃
            "H": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # h红桃
            "C": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # c方块
            "D": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],  # d梅花
        }
        self.play_cards = {
            '0': [],
            '1': [],
            '2': [],
            '3': [],
        }
        # 重置剩余牌的索引 1020
        self.remain_cards_classbynum = [8] * 13
        self.remain_cards_classbynum.append(2)
        self.remain_cards_classbynum.append(2)
        # end 1020
        # TODO: 选手可自行做出其他处理
        print("当前训练次数为{}, 设定的游戏次数为{}".format(self._curTimes, self._settingTimes))

    def notify_game_result(self):
        """
        到达指定游戏次数游戏结束，用于通知所有玩家游戏结束
        形如下所表示的JSON格式。该JSON表示经过2场对局后游戏结束，其中0号位玩家和2号位玩家胜利次数位2。
        {
            "type": "notify",
            "stage": "gameResult",
            "victoryNum": [2, 0, 2, 0]
            "draws": [0, 0, 0, 0]
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        print("达到设定场次, 其中0号位胜利{}次，1号位胜利{}次，2号位胜利{}次，3号位胜利{}次".format(*self._victoryNum))
        print("其中平局次数：0号位平局{}次，1号位平局{}次，2号位平局{}次，3号位平局{}次".format(*self._draws))

    def act_play(self):
        """
        出牌阶段，用于通知该玩家做出动作
        形如下所表示的JSON格式:
        {
            "type": "act",
            "handCards": [C3, D3, D3, H5, C5, D5, S6, D6 ... ] ,
            "publicInfo": [
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None}
            ],
            "selfRank": ‘2’,
            "oppoRank": ‘2’,
            "curRank": ‘2’,
            "stage": "play",
            "curPos": -1,
            "curAction": None,
            "greaterAction": -1,
            "greaterPos": None,
            "actionList": {"Single" : {'2': ['S2', 'S2' ...]} ...}
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        for i in range(4):
            if self._publicInfo[i]["playArea"] is None:
                self.play_cards[str(i)] = []
            else:
                self.play_cards[str(i)] = self._publicInfo[i]["playArea"][2]
        # TODO: 选手可自行做出其他处理
        print("我方等级：{}， 对方等级：{}， 当前等级{}".format(self._selfRank, self._oppoRank, self._curRank))
        print("当前动作为{}号-动作{}， 最大动作为{}号-动作{}".format(
            self._curPos, self._curAction, self._greaterPos, self._greaterAction)
        )


    def act_tribute(self):
        """
        进贡阶段，用于该玩家进贡
        形如下所表示的JSON格式:
        {
            "type": "act",
            "handCards": [C3, D3, D3, H5, C5, D5, S6, D6 ... ] ,
            "publicInfo": [
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None}
            ],
            "selfRank": ‘2’,
            "oppoRank": ‘3’,
            "curRank": ‘3’,
            "stage": "tribute",
            "curPos": -1,
            "curAction": None,
            "greaterAction": -1,
            "greaterPos": None,
            "actionList": {"tribute": ["S3"]}
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        print("我方等级：{}， 对方等级：{}， 当前等级{}".format(self._selfRank, self._oppoRank, self._curRank))
        print("轮到自己进贡，可进贡的牌有: ")

    def act_back(self):
        """
        还贡阶段，用于该玩家进贡
        形如下所表示的JSON格式:
        {
            "type": "act",
            "handCards": [C3, D3, D3, H5, C5, D5, S6, D6 ... ] ,
            "publicInfo": [
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None},
                {'rest': 27, 'playArea': None}
            ],
            "selfRank": ‘3’,
            "oppoRank": ‘2’,
            "curRank": ‘3’,
            "stage": "back",
            "curPos": -1,
            "curAction": None,
            "greaterAction": -1,
            "greaterPos": None,
            "actionList": {"back": ["S2", "D3"]}
        }
        请仅在对应的JSON格式下访问对应的实例属性，若此时访问其他属性则很有可能是之前处理时未更新的实例属性，不具有准确性。
        """
        # TODO: 选手可自行做出其他处理
        print("我方等级：{}， 对方等级：{}， 当前等级{}".format(self._selfRank, self._oppoRank, self._curRank))
        print("轮到自己还贡，可还贡的牌有:")

