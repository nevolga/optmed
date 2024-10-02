# Reproducing results from the paper Metabolic modelling as a powerful tool to identify critical components of _Pneumocystis_ growth medium

This repository contains all the necessary files and instructions to reproduce the results from the paper Metabolic modelling as a powerful tool to identify critical components of _Pneumocystis_ growth medium.

## Prerequisites
Before reproducing the results, the Digital Lab must be installed on-premises. Detailed installation instructions can be found [here](https://constellab.community/bricks/gws_academy/latest/doc/digital-lab/overview/294e86b4-ce9a-4c56-b34e-61c9a9a8260d). Please ensure that all installation steps are completed before proceeding to run the tasks. The installation guide for gws_gena is available [here](https://github.com/Constellab/gws_gena/tree/master?tab=readme-ov-file). Please use the recommended method through the Constellab platform. Input files from tests/data can be added as digital resources in the lab.

## How to Reproduce the results as described in Figures 5, 6, 7, and 8. 
All necessary input files and configurations are available in this repository. The following instructions describe the tasks to run for each figure, using the Digital Lab environment.

### Figure 5
To reproduce the results presented in Figure 5, follow these steps:

1. Run the _Transporter Adder_ Task

Configurations: None
Inputs:
- _network_min_model_Pmu_cyst_ as a Network
- _medium_glucose_, _medium_Merali_, or _medium_Merali_lipids_ as a Medium table

2. Run the _FBA Protocol_ Task

Configurations:
Biomass optimization: maximize
Solver: quad
Relax QSSA: true
QSSA relaxation coefficient: 1
Parsimony strength: 0
Inputs:
- Output from the _Transporter Adder_ task as a Network
- _context_ as a Context

### Figure 7
To reproduce the results shown in Figure 7, follow these steps:

1. Run the _Transporter Adder_ Task

Configurations: None
Inputs:
- _network_min_model_Pmu_cyst_ or _network_min_model_Pmu_cyst_no_SHMT_ as a Network
- _medium_Merali_no_ser_gly_ as a Medium table

2. Run the _FBA Protocol_ Task

Configurations:
Biomass optimization: maximize
Solver: quad
Relax QSSA: true
QSSA relaxation coefficient: 1
Parsimony strength: 0
Inputs:
- Output from the _Transporter Adder_ task as a Network
- _context_ as a Context

### Figures 6 & 8
To reproduce the results for Figures 6 & 8, follow these steps:

1. Run the _KOA Protocol_ Task

Configurations:
Biomass optimization: maximize
Multiple KO delimiter: ;
Solver: quad
Relax QSSA: true
QSSA relaxation coefficient: 1
Parsimony strength: 0
Inputs:
- _network_min_model_Pmu_cyst_Merali_ as a Network
- _context_ as a Context
- _ko_Merali_ as a KO table

2. Run the _KOA Results Extractor_ Task

Configurations:
Fluxes to extract: network_Biomass
Inputs:
Output from the _KOA Protocol_ task as a KOA result tables

# Medium Optimisation Reinforcement Learning Environment

## Overview

This project provides a custom reinforcement learning (RL) environment for medium optimisation using the Gym interface. The biomass computation is performed as implemented in the [gws_gena](https://github.com/Constellab/gws_gena) library for the [Constellab](https://constellab.io/). The project includes two main components:

1. `biomass_gym_env.py`: Defines the custom Gym environment, BiomassEnv, for medium optimisation.
2. `minimal_medium.py`: The MinimalMedium class is implemented as a task that can be run via Constellab UI. MinimalMedium employes the PPO algorithm (the implementation from [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/)) to interact with BiomassEnv and find the minimal irreducible subset of nutrients from the initial medium without dropping the biomass value.

## Usage

The installation guide for gws_gena is available [here](https://github.com/Constellab/gws_gena/tree/master?tab=readme-ov-file). Please use the recommended method through the Constellab platform. The current project can be installed in a similar way. Input files from tests/data can be added as digital resources in the lab (see [here](https://constellab.community/bricks/gws_academy/latest/doc/digital-lab/overview/294e86b4-ce9a-4c56-b34e-61c9a9a8260d)).

## License

This is licensed under the GNU General Public License v3.0.
