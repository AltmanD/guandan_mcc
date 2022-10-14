import time
from multiprocessing import Process

import pygame
import zmq
from pyarrow import deserialize, serialize
from pygame.locals import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.font = pygame.font.Font('showdown/fonts/HanYiRegular.ttf', 20)
        self.cards_image_path = 'showdown/images/cards/'
        self.background_image_path = 'showdown/images/background.png'
        self.partbackground_image_path = 'showdown/images/partback.bmp'
        self.chup_image_path = 'showdown/images/chup.png'
        self.buc_image_path = 'showdown/images/buc.png'
        self.chupImage = pygame.image.load(self.chup_image_path)
        self.bucImage = pygame.image.load(self.buc_image_path)
        self.backgroundImage = pygame.image.load(self.background_image_path)
        self.partback = pygame.image.load(self.partbackground_image_path)
        self.cardbackImage = pygame.image.load(self.cards_image_path + 'back.bmp')
        self.height = 900
        self.width = 1200

        waiting_image_path = 'showdown/images/waiting.png'
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        waitingImage = pygame.image.load(waiting_image_path).convert()
        self.screen.blit(pygame.transform.scale(waitingImage, (self.width, self.height)), (0, 0))  # 画等待
        pygame.display.update()
    
    def initInfo(self, message):
        self.my_handCards = message['handCards']
        self.curRank = message['curRank']
        self.selfRank = message['selfRank']
        self.oppRank = message['oppoRank']

    def showhandCards(self):    # 显示我方手牌
        self.screen.blit(pygame.transform.scale(self.backgroundImage, (self.width, self.height)), (0, 0))
        self.screen.blit(self.cardbackImage, (40, self.height/2-100))
        self.screen.blit(self.cardbackImage, (self.width-120, self.height/2-100))
        self.screen.blit(self.cardbackImage, (self.width/2-50, 30))
        self.base_width = (self.width - len(self.my_handCards) * 30)/2 - 50

        self.pokerImages = []
        for i, poker in enumerate(self.my_handCards):
            pokerImage = pygame.image.load(self.cards_image_path + poker + '.jpg').convert_alpha()    # (105,150)
            self.pokerImages.append(pokerImage)
            self.screen.blit(pokerImage, (self.base_width + i*30, self.height-200))
        pygame.display.update()

    def showpublicInfo(self):
        print(self.publicInfo)
        texts_positions = [(self.width/2, self.height-50), (self.width-120, self.height/2+30), (self.width/2-50, 160), (40, self.height/2+30)]
        cards_positions = [(self.width/2-100, self.height-500), (self.width-350, self.height/2-100), (self.width/2-100, 200), (150, self.height/2-100)]
        for i, (info, tpos, cpos) in enumerate(zip(self.publicInfo, texts_positions, cards_positions)):
            if i != 0:
                self.screen.blit(self.font.render(f"剩余{info['rest']}张牌", True, (0,0,0)), tpos)
            if info['playArea'] != None and info['playArea'][0] != None and info['playArea'][0] != 'PASS':
                for j, poker in enumerate(info['playArea'][2]):
                    if poker[0] != None:
                        pokerImage = pygame.image.load(self.cards_image_path + poker + '.jpg').convert_alpha()
                        self.screen.blit(pokerImage, (cpos[0] + j*30, cpos[1]))
        pygame.display.update()

    def updateInfo(self, message: dict):
        self.my_handCards = message['handCards']
        self.showhandCards()
        self.publicInfo = message['publicInfo']
        self.showpublicInfo()
        self.curRank = message['curRank']
        self.selfRank = message['selfRank']
        self.oppRank = message['oppoRank']

        self.curPos = message['curPos']
        self.curAction = message['curAction']
        self.greaterPos = message['greaterPos']
        self.greaterAction = message['greaterAction']

        self.legalActions = message['actionList']
        self.legalActions_set = []
        for action in self.legalActions[1:]:
            self.legalActions_set.append(set(action[2]))
        
    def waitInput(self):
        cards_up = []
        cards_down = list(range(len(self.pokerImages)))
        status_flag = 0
        action_choose = None
        action_index = None
        if len(self.legalActions) == 1:
            self.screen.blit(pygame.transform.scale(self.bucImage, (90, 40)), (self.width/2-30, self.height - 345))
            status_flag = 1
        elif ['PASS', 'PASS', 'PASS'] not in self.legalActions:
            self.screen.blit(pygame.transform.scale(self.chupImage, (90, 40)), (self.width/2-30, self.height - 345))
            status_flag = 2
        else:
            self.screen.blit(pygame.transform.scale(self.chupImage, (90, 40)), (self.width*2/3-30, self.height - 345))
            self.screen.blit(pygame.transform.scale(self.bucImage, (90, 40)), (self.width/3-30, self.height - 345))
            status_flag = 3
        pygame.display.update()

        while action_index is None:
            for event in pygame.event.get():
                print(event)
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                elif event.type == MOUSEBUTTONUP:
                    # 点击扑克牌
                    print(x, y)
                    self.screen.blit(pygame.transform.scale(self.partback, (self.width, self.height/3)), (0, self.height*2/3))
                    if self.height-230 <= y <= self.height-50 and self.base_width <= x <= self.base_width+len(self.pokerImages)*30+75:
                        if self.base_width+len(self.pokerImages)*30+75 - x < 105:
                            card_index = len(self.pokerImages)-1
                        else:
                            card_index = int((x - self.base_width) // 30)
                        if card_index in cards_down and card_index not in cards_up:
                            cards_down.remove(card_index)
                            cards_up.append(card_index)
                        elif card_index in cards_up and card_index not in cards_down:
                            cards_up.remove(card_index)
                            cards_down.append(card_index)
                    elif self.height - 345 <= y <= self.height - 305:
                        if status_flag == 1 and self.width/2-30 <= x <= self.width/2+60:
                            action_choose = ['PASS']
                            action_index = 0
                        elif status_flag == 2 and self.width/2-30 <= x <= self.width/2+60:
                            action_choose = []
                            for index in cards_up:
                                action_choose.append(self.my_handCards[index])
                        elif status_flag == 3:
                            if self.width/3-30 <= x <= self.width/3+60:
                                action_choose = ['PASS']
                                action_index = 0
                                cards_down.extend(cards_up)
                                cards_up = []
                            elif self.width*2/3-30 <= x <= self.width*2/3+60:
                                action_choose = []
                                for index in cards_up:
                                    action_choose.append(self.my_handCards[index])
                    print(action_choose)
                    if action_choose is not None and action_index is None:
                        if set(action_choose) in self.legalActions_set:
                            action_index = self.legalActions_set.index(set(action_choose))
                            cards_up = []
                        else:
                            cards_down.extend(cards_up)
                            cards_up = []
                            self.screen.blit(self.font.render(f"刚刚出的牌不符合规则", True, (0,0,0)), (self.width/2-90, self.height - 300))
                            action_choose = None

                    for i, card in enumerate(self.pokerImages):
                        if i in cards_up:
                            self.screen.blit(card, (self.base_width + i*30, self.height-230))
                        else:
                            self.screen.blit(card, (self.base_width + i*30, self.height-200))
                    pygame.display.update()
                if action_index is not None:
                    break
        return action_index


def run_one_player():
    board = Game()

    # 初始化zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{6003}')
    action_index = 0
    while True:
        message = deserialize(socket.recv())
        message = eval(message)
        if message['type'] == 'notify':
            if message['stage'] == 'beginning':
                board.initInfo(message)
        elif message['type'] == 'act':
            board.updateInfo(message)
            action_index = board.waitInput()
        print('choose action ', action_index, 'in this round')
        socket.send(serialize(action_index).to_buffer())

    action_index = 0
    file = open('showdown/test/test_message.log', 'r')
    messages = file.readlines()
    for message in messages:
        message = eval(message)
        if message['type'] == 'notify':
            if message['stage'] == 'beginning':
                board.initInfo(message)
        elif message['type'] == 'act':
            board.updateInfo(message)
            action_index = board.waitInput()
        # message = deserialize(socket.recv())
        print('choose action ', action_index, 'in this round')
        # socket.send(serialize(action_index).to_buffer())


def main():
    def exit_wrapper():
        """Exit all actors on KeyboardInterrupt (Ctrl-C)"""
        try:
            run_one_player()
        except KeyboardInterrupt:
            for _p in players:
                _p.terminate()

    players = []
    for i in [1]:
        p = Process(target=exit_wrapper)
        p.start()
        time.sleep(0.5)
        players.append(p)

    for player in players:
        player.join()

if __name__ == '__main__':
    main()
