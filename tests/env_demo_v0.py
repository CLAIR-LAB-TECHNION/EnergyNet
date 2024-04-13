
import sys
import os
import warnings
from typing import Mapping, List, Union, Any

# Add the project's root directory to sys.path
from energy_net.env.single_entity_v0 import gym_env
from energy_net.reward_function import RewardFunction
from tests.common import single_agent_cfgs


class HouseholdDummyRewardFunction(RewardFunction):
    r"""Dummy reward function class.

    Parameters
    ----------
    env_metadata: Mapping[str, Any]:
        General static information about the environment.
    **kwargs : dict
        Other keyword arguments for custom reward calculation.
    """

    def __init__(self, env_metadata: Mapping[str, Any], **kwargs):
        super().__init__(env_metadata, **kwargs)

    def calculate(self, observations: List[Mapping[str, Union[int, float]]]) -> List[float]:
        r"""Calculates reward.

        Parameters
        ----------
        observations: List[Mapping[str, Union[int, float]]]

        Returns
        -------
        reward: List[float]
            Reward for transition to current timestep.
        """
        # observation_seperator = importlib.import_module('utils.env_utils').observation_seperator
        return sum(d.consumption for d in observation_seperator(observations) if isinstance(d, ConsumerState))


def test_gym_api():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        for env_name, env_cfg in single_agent_cfgs.items():
            seed = hash(env_name)
            seed = abs(hash(str(seed)))
            env = gym_env(**env_cfg, initial_seed=seed)
            observation, info = env.reset()
            for _ in range(1000):
                action = env.action_space.sample()  # agent policy that uses the observation and info
                # print(action, "action")
                observation, reward, terminated, truncated, info = env.step(action)
                # print(observation, "obs")
                
                if terminated or truncated:
                    observation, info = env.reset()
                    
        env.close()



if __name__ == '__main__':
    test_gym_api()

