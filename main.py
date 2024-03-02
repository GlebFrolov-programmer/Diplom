import math

from experiment import Experiment
from ega import EGA
from nektar import Nektar


# test_ega = EGA(task=task,
#                size_population=10,
#                count_population=int(task.count_places**0.5),
#                # count_population=3,
#                selection="o",
#                mutation_chance=0.05,
#                count_switches_gen=2,
#                )


exp = Experiment(count_exp=3,

                 random_data=True,
                 nektar_size=8,

                 count_scout=50,
                 ambit=15,
                 depth_search=-1,

                 size_population=5,
                 count_population=int(math.factorial(8)**0.5),
                 # count_population=3,
                 selection="o",
                 mutation_chance=0.05,
                 count_switches_gen=2,

                 system='mac'
                 )
