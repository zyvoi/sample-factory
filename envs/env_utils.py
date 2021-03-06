from utils.utils import is_module_available, log
from functools import wraps
from time import sleep


class EnvCriticalError(Exception):
    pass


def vizdoom_available():
    return is_module_available('vizdoom')


def minigrid_available():
    return is_module_available('gym_minigrid')


def quadrotors_available():
    return is_module_available('gym_art')


def dmlab_available():
    return is_module_available('deepmind_lab')


def voxel_env_available():
    return is_module_available('voxel_env')


def retry(exception_class=Exception, num_attempts=3, sleep_time=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(num_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_class as e:
                    if i == num_attempts - 1:
                        raise
                    else:
                        log.error('Failed with error %r, trying again', e)
                        sleep(sleep_time)

        return wrapper

    return decorator


class RewardShapingInterface:
    def __init__(self):
        pass

    def get_default_reward_shaping(self):
        """Should return a dictionary of string:float key-value pairs defining the current reward shaping scheme."""
        raise NotImplementedError

    def get_current_reward_shaping(self, agent_idx: int):
        raise NotImplementedError

    def set_reward_shaping(self, reward_shaping: dict, agent_idx: int):
        """
        Sets the new reward shaping scheme.
        :param reward_shaping dictionary of string-float key-value pairs
        :param agent_idx: integer agent index (for multi-agent envs)
        """
        raise NotImplementedError


def get_default_reward_shaping(env):
    """
    The current convention is that when the environment supports reward shaping, the env.unwrapped should contain
    a reference to the object implementing RewardShapingInterface.
    We use this object to get/set reward shaping schemes generated by PBT.
    """

    if hasattr(env.unwrapped, 'reward_shaping_interface'):
        if isinstance(env.unwrapped.reward_shaping_interface, RewardShapingInterface):
            return env.unwrapped.reward_shaping_interface.get_default_reward_shaping()

    return None


def set_reward_shaping(env, reward_shaping: dict, agent_idx: int):
    if hasattr(env.unwrapped, 'reward_shaping_interface'):
        if isinstance(env.unwrapped.reward_shaping_interface, RewardShapingInterface):
            env.unwrapped.reward_shaping_interface.set_reward_shaping(reward_shaping, agent_idx)
