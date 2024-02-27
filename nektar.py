from itertools import permutations
import random


class Nektar:
    def __init__(self, n: int, random_data=False):
        self.name = 'Nektar'
        self.works = self.gen_n(n)  # множество работ подлежащих выполнению
        self.nektar_places = self.gen_all_variants(self.works)  # все возможные комбинации перестановок работ
        self.count_places = len(self.nektar_places)  # количество перестановок
        if random_data:
            self.vec_T = self.random_fill_vec(choose_vec="vec_T", len_vec=n)  # вектор длительностей выполнений работ
            self.vec_d = self.random_fill_vec(choose_vec="vec_d", len_vec=n)  # вектор моментов поступлений работ
            self.vec_D = self.random_fill_vec(choose_vec="vec_D", len_vec=n)  # вектор директивных сроков
            self.vec_F = self.random_fill_vec(choose_vec="vec_F", len_vec=n)  # вектор коэффициентов штрафов
        else:
            self.vec_T = self.not_random_fill_vec(choose_vec="vec_T", slice=n)  # вектор длительностей выполнений работ
            self.vec_d = self.not_random_fill_vec(choose_vec="vec_d", slice=n)  # вектор моментов поступлений работ
            self.vec_D = self.not_random_fill_vec(choose_vec="vec_D", slice=n)  # вектор директивных сроков
            self.vec_F = self.not_random_fill_vec(choose_vec="vec_F", slice=n)  # вектор коэффициентов штрафов

    # Генерируется набор N работ
    @staticmethod
    def gen_n(n: int) -> list:
        return [str(i) for i in range(1, n + 1)]

    # Генерируются все перестановки
    @staticmethod
    def gen_all_variants(word: list) -> list:
        return list(permutations(word))

    # Вывод массива
    @staticmethod
    def print_list(array: list) -> None:
        for i in array:
            print(i)

    # Вывод нектара
    def print_nektar(self) -> None:
        print(f'---{self.name = }---',
              f'{self.works = }',
              f'{len(self.nektar_places) = }',
              f'{self.vec_T = }',
              f'{self.vec_d = }',
              f'{self.vec_D = }',
              f'{self.vec_F = }',
              sep='\n')

    @staticmethod
    def not_random_fill_vec(choose_vec: str, slice: int) -> list:

        # В зависимости от choose_vec задаем статически вектор со значениями, со срезом
        if choose_vec == "vec_T":
            return [5, 10, 5, 8, 7, 3, 6, 2, 10, 7][:slice]
        elif choose_vec == "vec_d":
            return [10, 4, 15, 0, 11, 17, 12, 6, 13, 5][:slice]
        elif choose_vec == "vec_D":
            return [14, 40, 20, 10, 30, 25, 13, 17, 39, 18][:slice]
        elif choose_vec == "vec_F":
            return [0.1, 0.5, 0.1, 0.2, 0.4, 0.7, 0.2, 0.1, 0.3, 0.1][:slice]

        return []

    @staticmethod
    def random_fill_vec(choose_vec: str, len_vec: int) -> list:

        # В зависимости от choose_vec генерируем вектор со значениями
        if choose_vec == "vec_T":
            return [random.randint(0, len_vec * 3) for i in range(len_vec)]
        elif choose_vec == "vec_d":
            return [random.randint(0, len_vec * 3) for i in range(len_vec)]
        elif choose_vec == "vec_D":
            return [random.randint(len_vec, len_vec * 5) for i in range(len_vec)]
        elif choose_vec == "vec_F":
            return [round(random.random(), 2) for i in range(len_vec)]

        return []
