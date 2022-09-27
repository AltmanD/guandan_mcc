import time
from multiprocessing import Process

import pygame
import zmq
from pyarrow import deserialize, serialize


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.font = pygame.font.Font('showdown/fonts/HanYiRegular.ttf', 40)
        self.cards_image_path = 'showdown/images/cards/'
        self.background_image_path = 'showdown/images/background.png'
        self.backgroundImage = pygame.image.load(self.background_image_path)
        self.cardbackImage = pygame.image.load(self.cards_image_path + 'back.bmp')
        self.height = 900
        self.width = 1200

        waiting_image_path = 'showdown/images/waiting.png'
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        waitingImage = pygame.image.load(waiting_image_path).convert()
        waitingImage_resize = pygame.transform.scale(waitingImage, (self.width, self.height))
        self.screen.blit(waitingImage_resize, (0, 0))  # 画等待
        pygame.display.update()
    
    def initInfo(self, message):
        self.my_handCards = message['handCards']
        self.curRank = message['curRank']
        self.selfRank = message['selfRank']
        self.oppRank = message['oppoRank']

    def showhandCards(self):    # 显示我方手牌
        self.screen.blit(pygame.transform.scale(self.backgroundImage, (self.width, self.height)), (0, 0))
        self.screen.blit(self.cardbackImage, (40, self.height/2-100))
        self.screen.blit(self.cardbackImage, (self.width-100, self.height/2-100))
        self.screen.blit(self.cardbackImage, (self.width/2-50, 30))
        base_width = (self.width - len(self.my_handCards) * 30)/2 - 50
        for i, poker2 in enumerate(self.my_handCards):
            poker_outhand = pygame.image.load(
                self.cards_image_path + poker2 + '.jpg').convert_alpha()
            self.screen.blit(poker_outhand, (base_width + i*30, self.height-200))
        pygame.display.update()

    def showpublicInfo(self):
        print(self.publicInfo)
        self.myInfo = self.publicInfo[0]
        self.nexInfo = self.publicInfo[1]
        self.oppInfo = self.publicInfo[2]
        self.preInfo = self.publicInfo[3]
        
        self.screen.blit(self.font.render("按下Q退出", True, (255, 255, 0)), (self.width/2, self.height/2))
        
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
        
    def waitInput(self):
        return 0


def run_one_player():
    board = Game()

    # # 初始化zmq
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # socket.bind(f'tcp://*:{6003}')

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
