from bees.bee import Bee
from nektar import Nektar
import random


class ScoutBee(Bee):
    def __init__(self, target: Nektar, ambit: int):
        super().__init__(target.works)
        self.name = 'ScoutBee'
        self.nektar = target
        self.place, self.places_around = self.get_places(target=target, ambit=ambit)
        self.best_place = self.get_answer(self.place)
        self.vec_X = self.best_place[1]
        self.vec_Y = self.best_place[2]
        self.penalty = self.best_place[3]
        self.sum_penalty = self.best_place[4]
        self.ambit = ambit

    def get_answer(self, place):
        answer = []
        for ind, i in enumerate(place):
            I = int(i) - 1

            if self.vec_Y[ind - 1] <= self.nektar.vec_d[I] or ind == 0:
                self.vec_X[ind] = self.nektar.vec_d[I]
                self.vec_Y[ind] = self.nektar.vec_d[I] + self.nektar.vec_T[I]
            else:
                self.vec_X[ind] = self.vec_Y[ind - 1]
                self.vec_Y[ind] = self.vec_Y[ind - 1] + self.nektar.vec_T[I]

            # начисляется штраф, если не выполняется в срок
            if self.vec_Y[ind] > self.nektar.vec_D[I]:
                self.penalty[ind] = round(self.nektar.vec_F[I] * (self.vec_Y[ind] - self.nektar.vec_D[I]), 1)

        # генерируем list с ответом
        answer = [list(place), self.vec_X, self.vec_Y, self.penalty, round(sum(self.penalty), 2)]

        # зануляем изменяемые параметры
        self.vec_X = [0 for i in range(len(self.nektar.works))]
        self.vec_Y = [0 for i in range(len(self.nektar.works))]
        self.penalty = [0 for i in range(len(self.nektar.works))]

        return answer

    def get_places(self, target: Nektar, ambit: int):
        l = len(target.nektar_places)
        point = random.randint(0, l-1)
        place = list(target.nektar_places[point])

        # проверка на левую границу
        if point < ambit:
            places_around = [list(i) for i in target.nektar_places[:ambit*2]]
        # проверка на правую границу
        elif point > l - ambit:
            places_around = [list(i) for i in target.nektar_places[l-ambit*2:]]
        # по центру
        else:
            places_around = [list(i) for i in target.nektar_places[point-ambit:point+ambit]]

        s = []
        for p in places_around:
            s.append(self.get_answer(p))

        return place, s


    def print_bee(self) -> None:
        print(f'---{self.name = }---',
              f'Count of works: {len(self.vec_X)}',
              f'{self.place = }',
              f'{self.vec_X = }',
              f'{self.vec_Y = }',
              f'{self.penalty = }',
              f'{self.sum_penalty = }',
              f'{self.ambit = }',
              f'{self.places_around = }',
              sep='\n')

    # краткая статистика
    def print_statistic(self):
        print()
        print(f'F = {self.sum_penalty}',
              f'Place = {self.place}',
              sep='\n')
        print()
