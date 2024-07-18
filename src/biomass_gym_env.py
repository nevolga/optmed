# Gencovery software - All rights reserved
# This software is the exclusive property of Gencovery SAS.
# The use and distribution of this software is prohibited without the prior consent of Gencovery SAS.
# About us: https://gencovery.com

import numpy as np
import pandas as pd
import gym
import math
from gym import spaces


from gws_gena import (FBAResult, Twin, ReconHelper)
from gws_gena.fba.fba_helper.fba_helper import FBAHelper


class BiomassEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render.modes": ["human"]}

    def __init__(self, nutrients=np.ones(155), biomass_threshold=1, input_specs=None,
                 action_masks=None):
        super().__init__()


        self.input_specs = input_specs
        self.nutrients = nutrients
        self.max_n = len(self.nutrients)

        if action_masks is None:
            self.default_action_masks = np.full((self.max_n + 1,), True)
        else:
            self.default_action_masks = action_masks.copy()

        self._action_masks = self.default_action_masks.copy()
        self.render_mode = "console"
        self.biomass_threshold = biomass_threshold
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.max_n + 1,), dtype=np.float32)

        self.action_space = spaces.Discrete(self.max_n + 1)
        self._history = pd.DataFrame(columns=['nutrients',
                                              'nutrients_num',
                                              'reward',
                                              'biomass',
                                              'trial_biomass',
                                              'removed_nutrient',
                                              'result'])

        self.max_biomass = self.biomass = self.calculate_biomass(self.nutrients_to_list())

        # Define initial state of the system
        self.reset()


    def step(self, action):

        # check if action is to terminate episode
        if action == self.max_n:
            return self.observation(), 0, True, False, {}

        # check if we can't remove this nutrient
        # because it is already removed
        # or its removing was rejected earlier
        if not self._action_masks[action]:
            return self.observation(), 0, False, False, {}

        nutrients = self.nutrients_to_list()
        nutrients.remove(action)
        new_biomass = self.calculate_biomass(nutrients)

        # calculate the reward
        reward = 1 / self.max_n

        self._action_masks[action] = False

        # check if any action is still available
        # if not the episode will be terminated
        terminate = not any(self._action_masks)

        # if biomass is below threshold
        # we reject the nutrient removing
        threshold = self.max_biomass * self.biomass_threshold
        if (new_biomass < threshold) and not (math.isclose(new_biomass, threshold, rel_tol=1e-5)):
            
            self.add_step_to_table(0, 'R', new_biomass, removed_nutri=action)
            return self.observation(), 0, terminate, False, {}

        # if we accept nutrient removing
        # update biomass and nutrient coordinate
        self.biomass = new_biomass
        self.nutrients[action] = 0

        self.add_step_to_table(reward, 'A', new_biomass, removed_nutri=action)
        return self.observation(), reward, terminate, False, {}


    def reset(self, seed=None, options=None):

        self.nutrients = np.ones(self.max_n)
        self.biomass = self.max_biomass
        self._action_masks = self.default_action_masks.copy()

        self.add_step_to_table(0, 'A', self.max_biomass)

        return self.observation(), {}


    def render(self, mode="console"):

        print(f'N nutrients: {sum(self.nutrients)}, Observation: {self.observation()}')


    def action_masks(self):

        return self._action_masks


    def observation(self):

        return np.concatenate((self.nutrients, [self.biomass]))


    # Adds the line [nutrients, biomass, A] to the history dataframe
    def add_step_to_table(self, reward, result, biomass, removed_nutri=None):

        nutrients = self.nutrients_to_list()
        # print(f'Nutrients: {nutrients}, '
        #       f'Reward: {reward}, '
        #       f'Removed_nutrient: {removed_nutri}, '
        #       f'Result: {result}, '
        #       f'Nutrients_num: {len(nutrients)}, ')
        self._history.loc[len(self._history)]=[nutrients, len(nutrients), reward, self.biomass, biomass, removed_nutri, result]


    # returns history as dataframe
    def history(self):

        return self._history


    # returns nutrients as the list of nutrients numbers
    def nutrients_to_list(self):
        return [i for i, e in enumerate(self.nutrients) if e != 0]


    # biomass calculation
    # nutrients contains the list of nutrient set
    def calculate_biomass(self, nutrients):

        # parameters should be updated according to the given nutrients list <nutrients>
        net = self.input_specs["network"].copy()
        medium_table = self.input_specs['medium_table']
        context = self.input_specs['context']

        medium_table_current = medium_table.select_by_row_indexes(nutrients)

        # calling a task  BiomassFunction to calculate biomass
        helper = ReconHelper()
        helper.add_medium_to_network(net, medium_table_current)

        twin = Twin()
        twin.add_network(net)
        twin.add_context(context, related_network=net)

        solver = "quad"
        biomass_optimization = "maximize"
        fluxes_to_maximize = None
        fluxes_to_minimize = None
        relax_qssa = True
        qssa_relaxation_strength = 1
        parsimony_strength = 0

        helper = FBAHelper()
        fba_result: FBAResult = helper.run(
            twin, solver, fluxes_to_maximize, fluxes_to_minimize, biomass_optimization=biomass_optimization,
            relax_qssa=relax_qssa, qssa_relaxation_strength=qssa_relaxation_strength,
            parsimony_strength=parsimony_strength)

        # retrieve simulation values
        df = fba_result.get_flux_dataframe_by_reaction_ids("network_Biomass")
        values = df.iloc[0].tolist()
        biomass_new = values[0]

        return biomass_new
