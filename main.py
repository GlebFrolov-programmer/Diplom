import math
from experiment import Experiment
from multiprocessing import freeze_support


def main():
    nektar_size = 10
    Experiment(count_exp=10,

               random_data=True,
               nektar_size=nektar_size,

               count_scout=85,
               ambit=55,
               depth_search=-1,

               size_population=int(math.factorial(nektar_size)**0.25),
               count_population=int(math.factorial(nektar_size)**0.5),
               selection="r",
               mutation_chance=0.05,
               count_switches_gen=2,

               system='windows',
               count_stream=5,
               )


if __name__ == "__main__":
    freeze_support()
    main()
