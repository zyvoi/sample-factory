from os.path import join

from utils.utils import project_root


def add_eval_args(parser):
    parser.add_argument('--fps', default=0, type=int, help='Enable sync mode with adjustable FPS. Default (0) means default, e.g. for Doom its FPS (~35), or unlimited if not specified by env. Leave at 0 for Doom multiplayer evaluation')
    parser.add_argument('--evaluation_env_frameskip', default=1, type=int, help='Environment frameskip during evaluation. Leave at 1 (default) for the smoothest rendering')
    parser.add_argument('--render_action_repeat', default=None, type=int, help='Repeat an action that many frames during evaluation. By default uses the value from env config (used during training).')
    parser.add_argument('--record_to', default=join(project_root(), '..', 'recorded_episodes'), type=str, help='Record episodes to this folder')
    parser.add_argument('--no_render', action='store_true', help='Do not render the environment during evaluation')