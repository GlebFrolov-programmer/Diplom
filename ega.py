# from ega_algorithm.mutation import Mutation
import datetime

from nektar import Nektar
import random
import time


class EGA:

    def __init__(self, task: Nektar,
                 size_population: int,
                 count_population: int,
                 selection: str,
                 mutation_chance: float,
                 count_switches_gen: int,
                 ):

        start_time = time.time()
        self.task = task
        self.vec_T = task.vec_T
        self.vec_d = task.vec_d
        self.vec_D = task.vec_D
        self.vec_F = task.vec_F
        self.size_population = size_population
        self.start_population = self.get_population(task=self.task,
                                                    size_population=size_population,
                                                    method_generation='i',
                                                    )[:size_population]
        for i in range(count_population):
            if i == 0:
                self.next_generation = self.start_population

            # Selection
            if selection == 'o':
                self.selection = self.outbreeding_selection(self.next_generation.copy())
            elif selection == 'r':
                self.selection = self.random_selection(self.next_generation.copy())
            else:
                raise ValueError('Choose selection: "o" - outbreeding, "r" - random')

            # Crossbreeding
            children_population = self.cx_crossbreeding(self.selection)

            # Mutation childrens
            mutation_children = self.mutation(children=children_population,
                                              chance=mutation_chance,
                                              count_switches_gen=count_switches_gen)

            # Next population
            if i != count_population - 1:
                self.next_generation = self.generate_next_population(parents=self.next_generation,
                                                                     children=mutation_children,
                                                                     proportion=(1, 1, 1),
                                                                     last=False)
            else:
                self.next_generation = self.generate_next_population(parents=self.next_generation,
                                                                     children=mutation_children,
                                                                     proportion=(1, 1, 1),
                                                                     last=True)

        self.sort_population(self.next_generation)
        self.ega_time = time.time() - start_time

    # Получение популяции на равномерно распределенном интервале
    @staticmethod
    def get_population(task: Nektar, size_population: int = None, method_generation: str = 'r') -> list:

        if size_population is None:
            size_population = int(task.count_places**0.5)
        if size_population > task.count_places:
            raise ValueError('size_population не может превышать task.count_places')

        new_population = []
        if method_generation == 'i':
            interval = task.count_places // size_population
            for i in range(0, task.count_places, interval):
                new_population.append(task.nektar_places[i])
        elif method_generation == 'r':
            indexes = random.sample(range(0, task.count_places), size_population)
            for i in indexes:
                new_population.append(task.nektar_places[i])
        else:
            raise ValueError(f'Параметр method_generation должен быть: "r" или "i" (получено {method_generation})')

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
    @staticmethod
    def sort_population(l: list, k=-1) -> list:
        for i in range(len(l) - 1):
            for j in range(len(l) - i - 1):
                if l[j][k] > l[j + 1][k]:
                    l[j], l[j + 1] = l[j + 1], l[j]
        return l

    # выбор пары методом аутбридинг
    @staticmethod
    def outbreeding_selection(l: list) -> list[list]:
        length = len(l) // 2
        parent_1 = l[:length]
        random.shuffle(parent_1)
        parent_2 = l[length:]
        random.shuffle(parent_2)

        outbreeding = []
        for i in range(length):
            outbreeding.append([parent_1[i], parent_2[i]])

        return outbreeding

    # выбор пары методом случайный
    @staticmethod
    def random_selection(l: list) -> list[list]:
        random.shuffle(l)

        random_selection = []
        for i in range(0, len(l) - 1, 2):
            random_selection.append([l[i], l[i + 1]])

        return random_selection

    # СХ алгоритм скрещивания
    def cx_crossbreeding(self, parents: list[list]) -> list:
        new_population = []
        for parent_pair in parents:
            l = len(parent_pair[0])
            parents_dict = self.arrays_to_dict(parent_pair[0], parent_pair[1])
            cycles = []
            used_values = []
            index = self.start_cycle(parents_dict, used_values)
            while len(used_values) != l:
                cycle = []
                pos_1 = index
                pos_2 = parents_dict[index]
                used_values.append(pos_1)
                if pos_1 == pos_2:
                    cycles.append([index])
                else:
                    start_pos = pos_1
                    cycle.append(start_pos)
                    while start_pos != pos_2:
                        pos_1 = pos_2
                        pos_2 = parents_dict[pos_1]
                        cycle.append(pos_1)
                        used_values.append(pos_1)
                    cycles.append(cycle)

                index = self.start_cycle(parents_dict, used_values)

            for i in self.switch_cycles_pairs(cycles, parent_pair):
                new_population.append(i)

        return new_population

    @staticmethod
    def arrays_to_dict(l1: list | tuple, l2: list | tuple) -> dict:
        dictionary = dict()
        for i in range(len(l1)):
            dictionary[int(l1[i])] = int(l2[i])

        return dictionary

    @staticmethod
    def start_cycle(dictionary: dict, used_values: list):
        for d in dictionary:
            if d not in used_values:
                return d
        return -1

    # ГДЕ-ТО ОШИБКА В ЭТОЙ ФУНКЦИИ
    @staticmethod
    def switch_cycles_pairs(cycles: list[list], pairs: list) -> list[list]:

        l = len(pairs[0])
        child_1 = ['0' for s in range(l)]
        child_2 = ['0' for s in range(l)]

        i = 0
        for cycle in cycles:
            len_added_items = 0
            if i % 2 == 0:
                for key in pairs[0]:
                    if int(key) in cycle:
                        ind = pairs[0].index(key)
                        child_1[ind] = pairs[1][ind]
                        child_2[ind] = pairs[0][ind]
                        len_added_items += 1
                        if len_added_items == len(cycle):
                            break
            else:
                for key in pairs[0]:
                    if int(key) in cycle:
                        ind = pairs[0].index(key)
                        child_1[ind] = pairs[0][ind]
                        child_2[ind] = pairs[1][ind]
                        len_added_items += 1
                        if len_added_items == len(cycle):
                            break
            i += 1

        return [child_1, child_2]

    def mutation(self, children: list, chance: float, count_switches_gen: int) -> list:

        for i in range(len(children)):
            if random.random() <= chance:
                children[i] = self.switch_gens(children[i], count_switches_gen)

        return [tuple(i) for i in children]

    @staticmethod
    def switch_gens(child: list | tuple, count: int) -> list | tuple:
        for i in range(count):
            index_1, index_2 = random.sample(range(len(child)), 2)

            temp = child[index_1]
            child[index_1] = child[index_2]
            child[index_2] = temp

        return child

    def generate_next_population(self, parents: list,
                                 children: list,
                                 proportion: tuple = (1, 1, 1),
                                 last: bool = False) -> list:
        '''proportion = [parents, children, other population]'''
        next_population = []
        proportion = [i/sum(proportion) for i in proportion]

        # если последняя популяция, то возвращаем объекты с решениями, иначе просто перестановки
        if last:
            parents_list = self.sort_population([self.get_answer(i) for i in parents])[
                           :int(self.size_population//2)]
            children_list = self.sort_population([self.get_answer(i) for i in children])[
                            :int(self.size_population//2)]
            # проверка на дубликаты
            for j in parents_list + children_list:
                if j not in next_population:
                    next_population.append(j)

            return next_population

            # length = self.size_population - len(parents_list) - len(children_list)
            # while length != 0:
            #     ind = random.randint(0, self.task.count_places)
            #
            #     if self.get_answer(self.task.nektar_places[ind]) not in next_population:
            #         next_population.append(self.get_answer(self.task.nektar_places[ind]))
            #         length -= 1
        else:
            parents_list = self.sort_population([self.get_answer(i) for i in parents])[
                           :int(self.size_population * proportion[0])]
            children_list = self.sort_population([self.get_answer(i) for i in children])[
                            :int(self.size_population * proportion[0])]

            # проверка на дубликаты
            for j in [i[0] for i in parents_list] + [i[0] for i in children_list]:
                if j not in next_population:
                    next_population.append(j)

            length = self.size_population - len(parents_list) - len(children_list)
            while length != 0:
                ind = random.randint(0, self.task.count_places-1)
                if list(self.task.nektar_places[ind]) not in next_population:
                    next_population.append(self.task.nektar_places[ind])
                    length -= 1
        return next_population

    # вывод лучших решений
    def print_results(self, line_after_print: bool = True) -> None:
        res = []
        best_score = -1
        for i in self.next_generation:
            if best_score == -1 or best_score == i[-1]:
                best_score = i[-1]
                res.append(i)
            else:
                break

        print(f'EGA ({self.ega_time}): {res}')
        if line_after_print:
            print('-----------------------')






