# from ega_algorithm.mutation import Mutation
from nektar import Nektar


class Population:

    def __init__(self, task: Nektar | list, size_population: int):

        self.vec_X = [0 for i in range(len(task.works))]  # вектор моментов начала выполнения
        self.vec_Y = [0 for i in range(len(task.works))]  # вектор моментов окончания выполнения
        self.penalty = [0 for i in range(len(task.works))]  # вектор суммы штрафов за каждую работу
        self.sum_penalty = sum(self.penalty)
        self.places = self.get_population(task=task, size_population=size_population)
        self.vec_T = task.vec_T
        self.vec_d = task.vec_d
        self.vec_D = task.vec_D
        self.vec_F = task.vec_F
        self.sort_places()

    def get_population(self, task: Nektar, size_population: int = None) -> list:

        if size_population is None:
            size_population = int(task.count_places**0.5)

        new_population = []
        for i in range(0, task.count_places, size_population):
            new_population.append(self.get_answer(task.nektar_places[i]))

        return new_population

    def get_answer(self, place):
        answer = []
        for ind, i in enumerate(place):
            I = int(i) - 1

            if self.vec_Y[ind - 1] <= self.vec_d[I] or ind == 0:
                self.vec_X[ind] = self.vec_d[I]
                self.vec_Y[ind] = self.vec_d[I] + self.vec_T[I]
            else:
                self.vec_X[ind] = self.vec_Y[ind - 1]
                self.vec_Y[ind] = self.vec_Y[ind - 1] + self.vec_T[I]

            # начисляется штраф, если не выполняется в срок
            if self.vec_Y[ind] > self.vec_D[I]:
                self.penalty[ind] = round(self.vec_F[I] * (self.vec_Y[ind] - self.vec_D[I]), 1)

        # генерируем list с ответом
        answer = [list(place), self.vec_X, self.vec_Y, self.penalty, round(sum(self.penalty), 2)]

        # зануляем изменяемые параметры
        self.vec_X = [0 for i in range(len(self.vec_X))]
        self.vec_Y = [0 for i in range(len(self.vec_Y))]
        self.penalty = [0 for i in range(len(self.penalty))]

        return answer

    # Сортировка пузырьком двумерного массива по последнему полю
    def sort_places(self, k=-1) -> None:
        for i in range(len(self.places) - 1):
            for j in range(len(self.places) - i - 1):
                if self.places[j][k] > self.places[j + 1][k]:
                    self.places[j], self.places[j + 1] = self.places[j + 1], self.places[j]