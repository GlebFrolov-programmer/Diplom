from nektar import Nektar
# from ega_algorithm.selection import OutbreedingSelection, RandomSelection
from ega_algorithm.population import Population
# from ega_algorithm.crossbreeding import Crossbreeding
# from ega_algorithm.mutation import Mutation


class EGA:

    def __init__(self, task: Nektar,
                 count_population: int,
                 size_population: int,
                 selection: str,
                 chance_mutation: float):

        self.population = Population(task, size_population)
        # for i in range(count_population):
        #
        #     # Селекция
        #     if selection.lower() == 'o':
        #         self.selection = OutbreedingSelection(self.population)
        #     elif selection.lower() == 'r':
        #         self.selection = RandomSelection(self.population)
        #     else:
        #         raise ValueError('Choose selection: "o" - outbreeding, "r" - random')
        #
        #     # Скрещивание/кроссовер
        #     self.crossbreeding = Crossbreeding(self.selection)
        #
        #     # Мутация
        #     self.mutation = Mutation(self.crossbreeding, chance_mutation)
        #
        #     # Новая популяция
        #     self.population = Population(self.mutation, size_population)

