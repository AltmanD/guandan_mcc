import time
from multiprocessing import Process

import pygame
import zmq
from pyarrow import deserialize, serialize


class Game:
    def __init__(self) -> None:
        pygame.init()
        pass

    def update(self, message):
        pass

    def waitInput(self):
        pass


def run_one_player():
    board = Game()

    # 初始化zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{6003}')

    action_index = 0
    while True:
        message = deserialize(socket.recv())
        board.update(message)
        action_index = board.waitInput()
        socket.send(serialize(action_index).to_buffer())


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
        print(f'start{i}')
        p = Process(target=exit_wrapper)
        p.start()
        time.sleep(0.5)
        players.append(p)

    for player in players:
        player.join()

if __name__ == '__main__':
    main()
