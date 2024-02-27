from hive import Hive
import pandas as pd
import xlsxwriter
import os


class Experiment:

    def __init__(self,
                 nektar_size: int,
                 count_scout: int,
                 ambit: int,
                 depth_search: int,
                 count_exp: int,
                 random_data: bool):
        self.res_experimets = []
        self.nektar_size = nektar_size
        self.count_scout = count_scout
        self.ambit = ambit
        self.depth_search = depth_search
        self.count_exp = count_exp
        self.random_data = random_data

        for i in range(0, self.count_exp):
            print(f'======Hive {i + 1}======')
            h = Hive(nektar_size=self.nektar_size,
                     count_scout=self.count_scout,
                     ambit=self.ambit,
                     depth_search=self.depth_search,
                     random_data=self.random_data)

            h.print_best_bees()

            self.res_experimets.append({'forager_penalty': h.best_forager.sum_penalty,
                                        'master_penalty': h.master_bee.sum_penalty,
                                        'master_time': h.master_time,
                                        'forager_time': h.forager_time,
                                        'scout_time': h.scout_time
                                        })
            del h

        self.res_sum_penalty = [round(((i['forager_penalty'] - i['master_penalty'])/i['master_penalty']) * 100, 2) for i in self.res_experimets]
        self.res_time = [round((i['master_time']/(i['forager_time']+i['scout_time']))*100, 2) for i in self.res_experimets]
        self.sr_func = round(sum(self.res_sum_penalty)/len(self.res_sum_penalty), 2)
        self.sr_time = round(sum(self.res_time)/len(self.res_time), 2)

        self.table = self.create_dataframe()
        self.save_ta_excel(self.table)

    # Data frame of experiments
    def create_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame({'Относит. откл. (F)': self.res_sum_penalty,
                           'Относит. откл. (T)': self.res_time,
                           })
        df.loc[len(df.index)] = ['------------------------------------', '------------------------------------']
        df.loc[len(df.index)] = ['Ср. откл. (F -> 0%)', str(self.sr_func) + '%']
        df.loc[len(df.index)] = ['Ср. откл.(T > 100%)', str(self.sr_time) + '%']
        df.loc[len(df.index)] = ['------------------------------------', '------------------------------------']
        df.loc[len(df.index)] = ['Parameters:', ' ']
        df.loc[len(df.index)] = ['n', self.nektar_size]
        df.loc[len(df.index)] = ['count_scouts', self.count_scout]
        df.loc[len(df.index)] = ['ambit', self.ambit]
        df.loc[len(df.index)] = ['depth_search', self.depth_search]
        df.loc[len(df.index)] = ['random_data', self.random_data]

        print(f'Результат {self.count_exp} экспериментов:')
        print(df)

        return df

    # dataframe export to excel and save in exports directory
    @staticmethod
    def save_ta_excel(df: pd.DataFrame) -> None:
        current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file)
        path = current_directory + f'\\exports\\results_of_experiments.xlsx'
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Результаты алгоритмов', index=False)
        writer._save()
