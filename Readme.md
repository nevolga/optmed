# Reproducing results from the paper "Metabolic modelling as a powerful tool to identify critical components of _Pneumocystis_ growth medium"

This repository contains all the necessary files and instructions to reproduce the results from the paper "Metabolic modelling as a powerful tool to identify critical components of _Pneumocystis_ growth medium".

## Prerequisites
Before reproducing the results, a digital lab (developed by the [Constellab](https://constellab.io/)) must be created either on premises or in a cloud to run the code. Overview of the digital lab can be found [here](https://constellab.community/bricks/gws_academy/latest/doc/digital-lab/overview/294e86b4-ce9a-4c56-b34e-61c9a9a8260d). To register, use [this link](https://constellab.space/signup). Detailed installation instructions can be found [here](https://constellab.community/bricks/gws_academy/latest/doc/digital-lab/digital-lab-for-desktop/700a88e8-da5c-4e97-b6eb-86e1b26f73e4#tutoriel-en-fran%C3%A7ais-pour-installer-un-digital-lab-desktop). Please ensure that all installation steps are completed before proceeding to run the tasks. The installation guide for `gws_gena` (a [Constellab](https://constellab.io/) library developed for reconstruction and analysis of the metabolic networks) is available [here](https://github.com/Constellab/gws_gena/tree/master?tab=readme-ov-file). Please use the recommended method through the Constellab platform. Version 0.6.3 was used in this study, tag 6.3 in the code. Input files from tests/data can be used as digital resources in the Lab.

## How to reproduce the results as described in Figures 5, 6, 7, and 8. 
All necessary input files and configurations are available in this repository. The following instructions describe the tasks to run for each figure, using the digital lab environment.

### Figure 5
To reproduce the results presented in Figure 5, follow these steps:

1. Run the _Transporter Adder_ task

Configurations: None

Inputs:
- `network_min_model_Pmu_cyst` as a Network
- `medium_glucose`, `medium_Merali`, or `medium_Merali_lipids` as a Medium table

2. Run the _FBA Protocol_ task

Configurations:
- Biomass optimization: `maximize`
- Solver: `quad`
- Relax QSSA: `true`
- QSSA relaxation coefficient: `1`
- Parsimony strength: `0`

Inputs:
- Output from the _Transporter Adder_ task as a Network
- `context` as a Context

### Figure 7
To reproduce the results shown in Figure 7, follow these steps:

1. Run the _Transporter Adder_ task

Configurations: None

Inputs:
- `network_min_model_Pmu_cyst` or `network_min_model_Pmu_cyst_no_SHMT` as a Network
- `medium_Merali_no_ser_gly` as a Medium table

2. Run the _FBA Protocol_ task

Configurations:
- Biomass optimization: `maximize`
- Solver: `quad`
- Relax QSSA: `true`
- QSSA relaxation coefficient: `1`
- Parsimony strength: `0`

Inputs:
- Output from the _Transporter Adder_ task as a Network
- `context` as a Context

### Figures 6 & 8
To reproduce the results for Figures 6 & 8, follow these steps:

1. Run the _KOA Protocol_ task

Configurations:
- Biomass optimization: `maximize`
- Multiple KO delimiter: `;`
- Solver: `quad`
- Relax QSSA: `true`
- QSSA relaxation coefficient: `1`
- Parsimony strength: `0`

Inputs:
- `network_min_model_Pmu_cyst_Merali` as a Network
- `context` as a Context
- `ko_Merali` as a KO table

2. Run the _KOA Results Extractor_ task

Configurations:
- Fluxes to extract: `network_Biomass`

Inputs:
- Output from the _KOA Protocol_ task as a KOA result tables

## Medium Optimisation Reinforcement Learning Environment

### Overview

This project provides a custom reinforcement learning (RL) environment for medium optimisation using the Gym interface. The biomass computation is performed as implemented in the [gws_gena](https://github.com/Constellab/gws_gena) library for the [Constellab](https://constellab.io/). The project includes two main components:

1. `biomass_gym_env.py`: Defines the custom Gym environment, BiomassEnv, for medium optimisation.
2. `minimal_medium.py`: The MinimalMedium class is implemented as a task that can be run via Constellab UI. MinimalMedium employes the PPO algorithm (the implementation from [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/)) to interact with BiomassEnv and find the minimal irreducible subset of nutrients from the initial medium without dropping the biomass value.

### Usage

The current project can be installed in a similar way to how it was done for _gws_gena_. Input files from tests/data can be used as digital resources in the Lab.

## License

This is licensed under the GNU General Public License v3.0.
