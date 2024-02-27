from bees.bee import Bee
from nektar import Nektar


class MasterBee(Bee):
    def __init__(self, target: Nektar):
        super().__init__(target.works)
        self.name = 'MasterBee'
        self.nektar = target
        self.places = self.search_places()
        self.best_places = self.get_best_places(self.min_penalty_index())
        self.vec_X = self.best_places[0][1]
        self.vec_Y = self.best_places[0][2]
        self.penalty = self.best_places[0][3]
        self.sum_penalty = self.best_places[0][4]

    def search_places(self):
        answers = []
        for variant in self.nektar.nektar_places:
            for ind, i in enumerate(variant):
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

            # генерируем list с ответами
            answers.append([list(variant), self.vec_X, self.vec_Y, self.penalty, round(sum(self.penalty), 2)])

            # зануляем изменяемые параметры
            self.vec_X = [0 for i in range(len(self.nektar.works))]
            self.vec_Y = [0 for i in range(len(self.nektar.works))]
            self.penalty = [0 for i in range(len(self.nektar.works))]

        return answers

    def get_best_places(self, indexes: list):
        best_places = []
        for i in indexes:
            best_places.append(self.places[i])
        return best_places
