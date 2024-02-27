class Bee:

    def __init__(self, works: list):
        self.name = "Bee"
        self.vec_X = [0 for i in range(len(works))]  # вектор моментов начала выполнения
        self.vec_Y = [0 for i in range(len(works))]  # вектор моментов окончания выполнения
        self.penalty = [0 for i in range(len(works))]  # вектор суммы штрафов за каждую работу
        self.sum_penalty = sum(self.penalty)
        self.places = []
        self.best_places = []

    def print_bee(self) -> None:
        print(f'---{self.name = }---',
              f'Count of works: {len(self.vec_X)}',
              f'{self.vec_X = }',
              f'{self.vec_Y = }',
              f'{self.penalty = }',
              f'{self.sum_penalty = }',
              f'{self.best_places = }',
              sep='\n')

    # Вывод мест с нектаром
    def print_best_places(self) -> None:
        print('Best places with nektar:')
        for i in self.best_places:
            print(i)

    # Сортировка пузырьком двумерного массива по последнему полю
    def sort_places(self, k=-1) -> None:
        for i in range(len(self.places) - 1):
            for j in range(len(self.places) - i - 1):
                if self.places[j][k] > self.places[j + 1][k]:
                    self.places[j], self.places[j + 1] = self.places[j + 1], self.places[j]

    # Поиск наборов, где минимальный штраф. Возвращает набор индексов
    def min_penalty_index(self, k=-1) -> list:
        min_F = self.places[0][k]
        min_I = [0]

        for ind, i in enumerate(self.places):
            if i[-1] < min_F:
                min_F = i[-1]
                min_I = [ind]
            elif i[-1] == min_F and ind != 0:
                min_I.append(ind)
        return min_I

    # ==
    def __eq__(self, other):
        return True if self.vec_X == other.vec_X and self.vec_Y == other.vec_Y else False

    # !=
    def __ne__(self, other):
        return True if self.vec_X != other.vec_X or self.vec_Y != other.vec_Y else False

    # <
    def __lt__(self, other):
        return self.sum_penalty < other.sum_penalty

    # >
    def __gt__(self, other):
        return self.sum_penalty > other.sum_penalty

    # <=
    def __le__(self, other):
        return self.sum_penalty <= other.sum_penalty

    # >=
    def __ge__(self, other):
        return self.sum_penalty >= other.sum_penalty
