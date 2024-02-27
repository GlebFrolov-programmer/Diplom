from bees.bee import Bee
from bees.scout_bee import ScoutBee
from nektar import Nektar


class ForagerBee(Bee):
    def __init__(self, target: ScoutBee, nektar: Nektar, depth_search=-1):
        super().__init__(target.place)
        self.name = 'ForagerBee'
        self.nektar = nektar
        self.target = target
        self.trace_back = str(self.target.best_place[0]) + ' -> '
        self.count_moves = 0
        self.depth_search = depth_search  # -1 == unlimit search
        self.places = target.places_around
        self.best_places = self.bee_search_nektar()
        self.vec_X = self.best_places[1]
        self.vec_Y = self.best_places[2]
        self.penalty = self.best_places[3]
        self.sum_penalty = self.best_places[4]

    def bee_search_nektar(self):
        previos_best_place = self.target.best_place[0]
        best_place = self.search_best_place_in_ambit(self.places)
        index_perm = self.get_index_of_permutation(best_place)
        if previos_best_place != best_place[0]:
            self.count_moves += 1
            self.trace_back += str(best_place[0]) + ' -> '

        if self.depth_search == -1:
            while True:
                new_places = self.get_new_ambit(point=index_perm)
                new_best_place = self.search_best_place_in_ambit(new_places)
                if new_best_place[-1] < best_place[-1]:
                    best_place = new_best_place
                    self.trace_back += str(best_place[0]) + ' -> '
                    self.count_moves += 1
                    index_perm = self.get_index_of_permutation(best_place)
                else:
                    break
        else:
            for i in range(self.depth_search):
                new_places = self.get_new_ambit(point=index_perm)
                new_best_place = self.search_best_place_in_ambit(new_places)
                if new_best_place[-1] < best_place[-1]:
                    best_place = new_best_place
                    self.trace_back += str(best_place[0]) + ' -> '
                    self.count_moves += 1
                    index_perm = self.get_index_of_permutation(best_place)
                else:
                    break

        return best_place

    @staticmethod
    def search_best_place_in_ambit(places: list):
        best_place = []
        min_penalty = min([i for i in (j[-1] for j in places)])
        for place in places:
            if min_penalty == place[-1]:
                best_place = place
                break

        return best_place

    def get_new_ambit(self, point: int):

        # проверка на левую границу
        if point < self.target.ambit:
            places_around = [list(i) for i in self.nektar.nektar_places[:self.target.ambit * 2]]
        # проверка на правую границу
        elif point > self.nektar.count_places - self.target.ambit:
            places_around = [list(i) for i in
                             self.nektar.nektar_places[self.nektar.count_places - self.target.ambit * 2:]]
        # по центру
        else:
            places_around = [list(i) for i in
                             self.nektar.nektar_places[point - self.target.ambit:point + self.target.ambit + 1]]

        s = []
        for p in places_around:
            s.append(self.get_answer(p))

        return s

    def get_index_of_permutation(self, perm: list):
        for ind, i in enumerate(self.nektar.nektar_places):
            if list(i) == perm[0]:
                return ind
        return -1

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

    def print_bee(self) -> None:
        print(f'---{self.name = }---',
              f'Count of works: {len(self.vec_X)}',
              f'{self.vec_X = }',
              f'{self.vec_Y = }',
              f'{self.penalty = }',
              f'{self.sum_penalty = }',
              f'{self.best_places = }',
              f'{self.count_moves = }',
              f'{self.trace_back = }',
              sep='\n')

    # краткая статистика
    def print_statistic(self):
        print()
        print(f'F = {self.sum_penalty}',
              f'Place = {self.best_places}',
              f'Traceback = {self.trace_back}',
              f'Count of moves: {self.count_moves}',
              sep='\n')
        print()
