import os
from argparse import ArgumentParser
from player import MyClient
from utils.cmdline import parse_cmdline_kwargs


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
parser = ArgumentParser()
parser.add_argument('--alg', type=str, default='ppo', help='The RL algorithm')
parser.add_argument('--env', type=str,
                    default='PongNoFrameskip-v4', help='The game environment')
parser.add_argument('--round', type=int, default=10,
                    help='The number of total play')
parser.add_argument('--ip', type=str, default='127.0.0.1',
                    help='IP address of learner server')
parser.add_argument('--data_port', type=int, default=5000,
                    help='Learner server port to send training data')
parser.add_argument('--param_port', type=int, default=5001,
                    help='Learner server port to subscribe model parameters')
parser.add_argument('--model', type=str, default='accnn',
                    help='Training model')
parser.add_argument('--max_steps_per_update', type=int, default=128,
                    help='The maximum number of steps between each update')
parser.add_argument('--exp_path', type=str, default=None,
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--num_saved_ckpt', type=int, default=10,
                    help='Number of recent checkpoint files to be saved')
parser.add_argument('--max_episode_length', type=int,
                    default=1000, help='Maximum length of trajectory')
parser.add_argument('--config', type=str, default=None,
                    help='The YAML configuration file')
                    
parser.add_argument('--observation_space', type=int, default=None,
                    help='The YAML configuration file')
parser.add_argument('--action_space', type=int, default=None,
                    help='The YAML configuration file')


def main():
    # Parse input parameters
    args, unknown_args = parser.parse_known_args()
    args.num_steps = int(args.num_steps)
    unknown_args = parse_cmdline_kwargs(unknown_args)

    rounds = args.round
    os.system(f'guandan {rounds}')
    client = []
    try:
        for i in range(4):
            args.client_index = i
            client.append(MyClient(f'ws://127.0.0.1:9618/game/gd/client{i}', args, unknown_args))
            client[i].connect()
            client[i].run_forever()
    except KeyboardInterrupt:
        for i in range(4):
            client[i].close()


if __name__ == '__main__':
    main()
