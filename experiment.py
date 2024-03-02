import datetime
from hive import Hive
import pandas as pd
import xlsxwriter
import os
from ega import EGA
from nektar import Nektar


class Experiment:

    def __init__(self,
                 # Эксперимент
                 count_exp: int,

                 # Задача
                 random_data: bool,
                 nektar_size: int,

                 # Эвристика
                 count_scout: int,
                 ambit: int,
                 depth_search: int,

                 # ЭГА
                 size_population: int,
                 count_population: int,
                 selection: str,
                 mutation_chance: float,
                 count_switches_gen: int,

                 # ОС
                 system: str
                 ):

        self.res_experimets = []
        self.nektar_size = nektar_size
        self.count_scout = count_scout
        self.ambit = ambit
        self.depth_search = depth_search
        self.count_exp = count_exp
        self.random_data = random_data
        self.size_population = size_population
        self.count_population = count_population
        self.selection = selection
        self.mutation_chance = mutation_chance
        self.count_switches_gen = count_switches_gen

        for i in range(0, self.count_exp):
            print(f'======Hive {i + 1}======')
            task = Nektar(self.nektar_size, self.random_data)
            h = Hive(target=task,
                     count_scout=self.count_scout,
                     ambit=self.ambit,
                     depth_search=self.depth_search,
                     )

            ega = EGA(task=task,
                      size_population=self.size_population,
                      count_population=self.count_population,
                      selection=self.selection,
                      mutation_chance=self.mutation_chance,
                      count_switches_gen=self.count_switches_gen,
                      )

            self.print_results_of_exp(h, ega)

            self.res_experimets.append({
                                        # Эвристика
                                        'forager_penalty': h.best_forager.sum_penalty,
                                        'master_penalty': h.master_bee.sum_penalty,
                                        'master_time': h.master_time,
                                        'forager_time': h.forager_time,
                                        'scout_time': h.scout_time,

                                        # ЭГА
                                        'ega_penalty': ega.next_generation[0][-1],
                                        'ega_time': ega.ega_time,
                                        })
            del h, ega

        self.res_sum_penalty_hive = [round(((i['forager_penalty'] - i['master_penalty'])/i['master_penalty']) * 100, 2) for i in self.res_experimets]
        self.res_sum_penalty_ega = [round(((i['ega_penalty'] - i['master_penalty'])/i['master_penalty']) * 100, 2) for i in self.res_experimets]

        self.res_time_hive = [round((i['master_time']/(i['forager_time']+i['scout_time']))*100, 2) for i in self.res_experimets]
        self.res_time_ega = [round((i['master_time']/i['ega_time'])*100, 2) for i in self.res_experimets]

        self.sr_func_hive = round(sum(self.res_sum_penalty_hive)/len(self.res_sum_penalty_hive), 2)
        self.sr_func_ega = round(sum(self.res_sum_penalty_ega)/len(self.res_sum_penalty_ega), 2)

        self.sr_time_hive = round(sum(self.res_time_hive)/len(self.res_time_hive), 2)
        self.sr_time_ega = round(sum(self.res_time_ega)/len(self.res_time_ega), 2)

        self.table = self.create_dataframe()
        self.save_ta_excel(self.table, system=system)

    # Data frame of experiments
    def create_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame({'Относит. откл. (F) hive': self.res_sum_penalty_hive,
                           'Относит. откл. (T) hive': self.res_time_hive,
                           'Относит. откл. (F) ega': self.res_sum_penalty_ega,
                           'Относит. откл. (T) ega': self.res_time_ega,
                           })
        df.loc[len(df.index)] = ['--------------------------------' for i in range(4)]
        df.loc[len(df.index)] = ['Ср. откл. (F -> 0%) hive', str(self.sr_func_hive) + '%', '', '']
        df.loc[len(df.index)] = ['Ср. откл.(T > 100%) hive', str(self.sr_time_hive) + '%', '', '']
        df.loc[len(df.index)] = ['Ср. откл. (F -> 0%) ega', str(self.sr_func_ega) + '%', '', '']
        df.loc[len(df.index)] = ['Ср. откл.(T > 100%) ega', str(self.sr_time_ega) + '%', '', '']
        df.loc[len(df.index)] = ['--------------------------------' for i in range(4)]
        df.loc[len(df.index)] = ['Parameters:', '', '', '']
        df.loc[len(df.index)] = ['n', self.nektar_size, '', '']
        df.loc[len(df.index)] = ['count_scouts', self.count_scout, '', '']
        df.loc[len(df.index)] = ['ambit', self.ambit, '', '']
        df.loc[len(df.index)] = ['depth_search', self.depth_search, '', '']
        df.loc[len(df.index)] = ['random_data', self.random_data, '', '']
        df.loc[len(df.index)] = ['size_population', self.size_population, '', '']
        df.loc[len(df.index)] = ['count_population', self.count_population, '', '']
        if self.selection == 'o':
            df.loc[len(df.index)] = ['selection', 'outbreeding', '', '']
        elif self.selection == 'r':
            df.loc[len(df.index)] = ['selection', 'random', '', '']
        df.loc[len(df.index)] = ['mutation_chance', self.mutation_chance, '', '']
        df.loc[len(df.index)] = ['count_switches_gen', self.count_switches_gen, '', '']

        print(f'Результат {self.count_exp} экспериментов:')
        print(df)

        return df

    # dataframe export to excel and save in exports directory
    @staticmethod
    def save_ta_excel(df: pd.DataFrame, system: str = 'windows') -> None:
        current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file)
        path = ''
        if system.lower() == 'windows':
            path = current_directory + f'\\exports\\results_of_experiments_{datetime.date.today()}.xlsx'
        elif system.lower() == 'mac':
            path = current_directory + f'/exports/results_of_experiments_{datetime.date.today()}.xlsx'

        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Результаты алгоритмов', index=False)
        worksheet = writer.sheets['Результаты алгоритмов']
        worksheet.set_column('A:D', 18)
        writer._save()

    @staticmethod
    def print_results_of_exp(hive: Hive, ega: EGA):
        hive.print_best_bees(False)
        ega.print_results(False)
        print()
