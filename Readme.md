# Medium Optimisation Reinforcement Learning Environment

## Overview

This project provides a custom reinforcement learning (RL) environment for medium optimisation using the Gym interface. The biomass computation is performed as implemented in the [gws_gena](https://github.com/Constellab/gws_gena) library for the [Constellab](https://constellab.io/). The project includes two main components:

1. `biomass_gym_env.py`: Defines the custom Gym environment, BiomassEnv, for medium optimisation.
2. `minimal_medium.py`: The MinimalMedium class is implemented as a task that can be run via Constellab UI. MinimalMedium employes the PPO algorithm (the implementation from [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/)) to interact with BiomassEnv and find the minimal irreducible subset of nutrients from the initial medium without dropping the biomass value.

## Usage

The installation guide for gws_gena is available [here](https://github.com/Constellab/gws_gena/tree/master?tab=readme-ov-file). Please use the recommended method through the Constellab platform. The current project can be installed in a similar way. Input files from tests/data can be added as digital resources in the lab (see [here](https://constellab.community/bricks/gws_academy/latest/doc/digital-lab/overview/294e86b4-ce9a-4c56-b34e-61c9a9a8260d)).

## License

This is licensed under the GNU General Public License v3.0.
