import os
import time
from argparse import ArgumentParser
from multiprocessing import Process

from player import MyClient
from utils.cmdline import parse_cmdline_kwargs

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
parser = ArgumentParser()
parser.add_argument('--round', type=int, default=100,
                    help='The number of total play')
parser.add_argument('--model', type=str, default='custom_acmlp', 
                    help='Training model')
parser.add_argument('--ip', type=str, default='127.0.0.1',
                    help='IP address of learner server')
parser.add_argument('--data_port', type=int, default=5000,
                    help='Learner server port to send training data')
parser.add_argument('--param_port', type=int, default=5001,
                    help='Learner server port to subscribe model parameters')
parser.add_argument('--exp_path', type=str, default=None,
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--num_saved_ckpt', type=int, default=10,
                    help='Number of recent checkpoint files to be saved')
parser.add_argument('--observation_space', type=int, default=None,
                    help='The YAML configuration file')
parser.add_argument('--action_space', type=int, default=None,
                    help='The YAML configuration file')

def run_one_client(index, args, unknown_args,):
    args.client_index = index
    client = MyClient(f'ws://127.0.0.1:9618/game/gd/client{index}', args, unknown_args)
    print(f'client{client}')
    client.connect()
    client.run_forever()

def main():
    # Parse input parameters
    args, unknown_args = parser.parse_known_args()
    unknown_args = parse_cmdline_kwargs(unknown_args)

    # 启动server好像只能在脚本中处理？
    # rounds = args.round
    # p = Process(target=os.system(f'./guandan {rounds}'))
    # p.start()
    # p.join()

    # time.sleep(10)
    # print('start')
    # client封装
    def exit_wrapper(index, *x, **kw):
        """Exit all actors on KeyboardInterrupt (Ctrl-C)"""
        try:
            run_one_client(index, *x, **kw)
        except KeyboardInterrupt:
            if index == 0:
                for _i, _p in enumerate(client):
                    if _i != index:
                        _p.terminate()

    clients = []
    for i in range(4):
        print(f'start{i}')
        p = Process(target=exit_wrapper, args=(i, args, unknown_args))
        p.start()
        clients.append(p)

    for client in clients:
        client.join()


if __name__ == '__main__':
    main()
