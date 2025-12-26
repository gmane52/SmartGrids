# /PROYECTO/src
## GridDefinition
It's a dedicated python script for model the electrical system with panda power in the initial state. The PF of the loads and line parameters are calculated on it. Once the grid is generated it's exported to a csv file. 

This way, we always have the initial state of the grid and can generate diferent versions with diferent solutions aproches.

- The path where results are saved its HARDCODED. It's inside data folder. Note this if you want to change the folders name.

## Project.ipynb
The development of the project itself.

0. Load data and data cleaning:;
    - generate/load the grid ✅
    - load generation and comsumption profiles ✅
    - castering, re-naming, filtering, merging, normalising ✅
    - plot of generation and load profiles ✅

1. Study of the current system: Power Flow Study 1:
    - Load flow study (with const control on load and nuclear generation bc wind an solar still are not in the grid...) ✅
    - Network operating costs for one year 
    - Conclusions of part 1.

2. Upgrading the current network, phase 1:
    - Grid modifications, 5 new lines added (both type, single and double). New grid generated called "project_net_part2" ✅
    - Load flow study ✅
    - N-1 Criteria evaluated at all nodes and lines. Evaluated based on V_max/min and Loadmax. ✅
    - Losses calculation. ✅
    - Modifying voltage level study
    - Network operating costs for one year
    - Network investment costs
    - Conclusions

# /PROYECTO
## README.md



# TIPS
- Activar venv (bash):
source .venv/Scripts/activate

- Foto de todo lo instalado en el venv
pip freeze > requirements.txt
