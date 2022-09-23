import time
from multiprocessing import Process

import pygame
import zmq
from pyarrow import deserialize, serialize


class Game:
    def __init__(self) -> None:
        pygame.init()
        waiting_image_path = 'showdown/images/waiting.png'
        screen = pygame.display.set_mode((900, 600), 0, 32)
        waitingImage = pygame.image.load(waiting_image_path).convert()
        screen.blit(waitingImage, (0, 0))  # 画等待
        pygame.display.update()
    
    def initInfo(self, message):
        self.my_handCards = message['handCards']
        self.curRank = message['curRank']
        self.selfRank = message['selfRank']
        self.oppRank = message['oppoRank']

    def showhandCards(self):
        pass

    def showpublicInfo(self):
        pass

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
