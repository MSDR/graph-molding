To run, we recommend starting with demo.py. This script runs a simulation of the best results of evolution on different fitness functions.

To run analysis, see analysis.py. 

main.py contains three demos:
- The interstate demo allows you to run a mold a single time on the U.S. cities map. You can adjust the molds' chromosome here to see its effect. Also, any world in designed_worlds.py and any fitness function in fitness_functions.py can be substituted. It's fun to play with!
- The genetic algorithm demo runs evolution. If ckpt_folder is specified, the results will be saved there.
- The evolution demo runs a simulation of all mold checkpoints through evolution, so you can see it happen in real-time!