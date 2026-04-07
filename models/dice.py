import random

class Dice:
    def __init__(self):
        # Inicializa os dados
        self.value1 = 1
        self.value2 = 1

    def roll(self):
        # Sorteia dois números entre 1 e 6
        self.value1 = random.randint(1, 6)
        self.value2 = random.randint(1, 6)
        return self.value1, self.value2