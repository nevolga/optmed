# Gencovery software - All rights reserved
# This software is the exclusive property of Gencovery SAS.
# The use and distribution of this software is prohibited without the prior consent of Gencovery SAS.
# About us: https://gencovery.com test

from gws_core import (ConfigParams, InputSpec, IntParam,
                      OutputSpec, Table, Task, TaskInputs,
                      TaskOutputs, task_decorator)
from gws_gena import (Context, MediumTable, Network)

import numpy as np
import gym as gym

from .biomass_gym_env import BiomassEnv

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib import MaskablePPO


@task_decorator("MinimalMedium", human_name="Minimal medium",
                short_description="Minimal medium prediction by RL")
class MinimalMedium(Task):
    """
    Minimal medium task.

    This task runs a code to predict a minimal medium composition by using the PPO algorithm.
    All steps of the learning process are stored in the history table.

    """

    input_specs = {
        'network': InputSpec(Network),
        'medium_table': InputSpec(MediumTable),
        'context': InputSpec(Context)
    }
    output_specs = {'history': OutputSpec(Table)}
    config_specs = {'loops_n': IntParam(
        default_value='1', human_name="Number of iterations", short_description="The number of iterations")}

    def run(self, params: ConfigParams, inputs: TaskInputs) -> TaskOutputs:

        # number of iterations to perform
        loops_n = params["loops_n"]

        action_masks = np.full(156, True)
        action_masks[-1] = False
        env = BiomassEnv(nutrients=np.ones(155), action_masks=action_masks, input_specs=inputs)

        model = MaskablePPO(MaskableActorCriticPolicy, env, verbose=1)

        for i in range(10):
            model.learn(total_timesteps=loops_n, progress_bar=True)

        return {'history': Table(env.history())}
