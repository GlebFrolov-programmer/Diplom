import math
import time

from experiment import Experiment
from multiprocessing import Pool, freeze_support


def main():
    nektar_size = 10
    exp = Experiment(count_exp=25,

                     random_data=True,
                     nektar_size=nektar_size,

                     count_scout=100,
                     ambit=30,
                     depth_search=-1,

                     size_population=int(math.factorial(nektar_size)**0.25),
                     count_population=int(math.factorial(nektar_size)**0.5),
                     selection="o",
                     mutation_chance=0.05,
                     count_switches_gen=2,

                     system='mac',
                     count_stream=4,
                     )


if __name__ == "__main__":
    freeze_support()
    main()