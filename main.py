from experiment import Experiment
from ega import EGA
from nektar import Nektar

# exp = Experiment(nektar_size=8,
#                  count_scout=50,
#                  ambit=15,
#                  depth_search=-1,
#                  count_exp=100,
#                  random_data=True,
#                  )
task = Nektar(8)
test_ega = EGA(task=task,
               size_population=10,
               # count_population=int(task.count_places**0.5),
               count_population=1,
               selection="o",
               mutation_chance=0.05)
