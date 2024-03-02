import math
from experiment import Experiment

nektar_size = 9
exp = Experiment(count_exp=5,

                 random_data=True,
                 nektar_size=nektar_size,

                 count_scout=50,
                 ambit=15,
                 depth_search=-1,

                 size_population=3,
                 count_population=int(math.factorial(nektar_size)**0.5),
                 selection="o",
                 mutation_chance=0.05,
                 count_switches_gen=2,

                 system='mac'
                 )
