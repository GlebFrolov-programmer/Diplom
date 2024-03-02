from bees.scout_bee import ScoutBee
from bees.forager_bee import ForagerBee
from bees.master_bee import MasterBee
from nektar import Nektar
import time


class Hive:
    def __init__(self,
                 target: Nektar,
                 count_scout: int,
                 ambit: int,
                 depth_search: int,
                 ):
        self.nektar = target

        master_time_start = time.time()
        self.master_bee = MasterBee(target=self.nektar)
        master_time_end = time.time()
        self.master_time = master_time_end - master_time_start

        scout_time_start = time.time()
        self.scouts = [ScoutBee(target=self.nektar, ambit=ambit) for i in range(count_scout)]
        scout_time_end = time.time()
        self.scout_time = scout_time_end - scout_time_start

        forager_time_start = time.time()
        self.foragers = [ForagerBee(target=i, nektar=self.nektar, depth_search=depth_search) for i in self.scouts]
        forager_time_end = time.time()
        self.forager_time = forager_time_end - forager_time_start

        self.best_scout, self.best_forager = self.search_best_bees()

    def statistics(self) -> None:
        print('===Statistics===')
        self.nektar.print_nektar()
        self.master_bee.print_bee()
        print('Scouts:')
        for scout in self.scouts:
            scout.print_statistic()
        print('Foragers:')
        for forager in self.foragers:
            forager.print_statistic()

        self.print_best_bees()

        print(f'F(scouts, foragers) - F(master) = {self.best_forager.sum_penalty - self.master_bee.sum_penalty}')
        print(f'Time:',
              f'{self.master_time = }',
              f'{self.scout_time = }',
              f'{self.forager_time = }',
              sep='\n')
        print('===End statistics===')

    def search_best_bees(self):
        best_forager = self.foragers[0]
        for forager in self.foragers:
            if forager.sum_penalty < best_forager.sum_penalty:
                best_forager = forager

        best_scout = best_forager.target

        return best_scout, best_forager

    def print_best_bees(self, line_after_print: bool = True) -> None:
        print('-----| Best bees |-----')
        print(f'Master ({self.master_time}): {self.master_bee.best_places}')
        print(f'Scout ({self.scout_time}): {self.best_scout.best_place}')
        print(f'Forager ({self.forager_time}): {self.best_forager.best_places}')
        if line_after_print:
            print('-----------------------')