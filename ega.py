# from ega_algorithm.mutation import Mutation
from nektar import Nektar
import random

class EGA:

    def __init__(self, task: Nektar,
                 size_population: int,
                 count_population: int,
                 selection: str,
                 mutation_chance: float,
                 ):
        self.vec_T = task.vec_T
        self.vec_d = task.vec_d
        self.vec_D = task.vec_D
        self.vec_F = task.vec_F
        self.population = self.get_population(task=task, size_population=size_population)[:size_population]
        for i in range(count_population):

            # Selection
            if selection == 'o':
                self.selection = self.outbreeding_selection()
            elif selection == 'r':
                self.selection = self.random_selection(self.population.copy())
            else:
                raise ValueError('Choose selection: "o" - outbreeding, "r" - random')

            # Crossbreeding

        # self.sort_places()
        print(self.population)

    # Получение популяции на равномерно распределенном интервале
    @staticmethod
    def get_population(task: Nektar, size_population: int = None) -> list:

        if size_population is None:
            size_population = int(task.count_places**0.5)
        if size_population > task.count_places:
            raise ValueError('size_population не может превышать task.count_places')

        interval = task.count_places // size_population
        new_population = []
        for i in range(0, task.count_places, interval):
            new_population.append(task.nektar_places[i])

        return new_population

    @staticmethod
    def get_population_random(task: Nektar, size_population: int = None) -> list:

        if size_population is None:
            size_population = int(task.count_places ** 0.5)
        if size_population > task.count_places:
            raise ValueError('size_population не может превышать task.count_places')

        indexes = random.sample(range(0, task.count_places - 1), size_population)

        new_population = []
        for i in indexes:
            new_population.append(task.nektar_places[i])

        return new_population

    def get_answer(self, place):
        l = len(self.vec_T)
        vec_X = [0 for i in range(l)]  # вектор моментов начала выполнения
        vec_Y = [0 for i in range(l)]  # вектор моментов окончания выполнения
        penalty = [0 for i in range(l)]  # вектор суммы штрафов за каждую работу
        # sum_penalty = sum(penalty)
        # answer = []
        for ind, i in enumerate(place):
            I = int(i) - 1

            if vec_Y[ind - 1] <= self.vec_d[I] or ind == 0:
                vec_X[ind] = self.vec_d[I]
                vec_Y[ind] = self.vec_d[I] + self.vec_T[I]
            else:
                vec_X[ind] = vec_Y[ind - 1]
                vec_Y[ind] = vec_Y[ind - 1] + self.vec_T[I]

            # начисляется штраф, если не выполняется в срок
            if vec_Y[ind] > self.vec_D[I]:
                penalty[ind] = round(self.vec_F[I] * (vec_Y[ind] - self.vec_D[I]), 1)

        # генерируем list с ответом
        answer = [list(place), vec_X, vec_Y, penalty, round(sum(penalty), 2)]

        return answer

    # Сортировка пузырьком двумерного массива по последнему полю
    def sort_places(self, k=-1) -> None:
        for i in range(len(self.places) - 1):
            for j in range(len(self.places) - i - 1):
                if self.places[j][k] > self.places[j + 1][k]:
                    self.places[j], self.places[j + 1] = self.places[j + 1], self.places[j]

    # выбор пары методом аутбридинг
    def outbreeding_selection(self) -> list[list]:
        l = len(self.population) // 2

        outbreeding = []
        for i in range(l):
            outbreeding.append([self.population[i], self.population[i + l]])

        return outbreeding

    # выбор пары методом случайный
    @staticmethod
    def random_selection(l: list) -> list[list]:
        random.shuffle(l)

        random_selection = []
        for i in range(0, len(l) - 1, 2):
            random_selection.append([l[i], l[i + 1]])

        return random_selection
