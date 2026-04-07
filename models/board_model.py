class BoardModel:
    def __init__(self):
        # Representação lógica do tabuleiro (sem renderização)
        # 1 - Vermelho, 2 - Verde, 3 - Azul
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 4],
            [0, 1, 3, 2, 2, 3, 1, 4],
            [0, 3, 1, 3, 3, 1, 3, 4],
            [0, 2, 3, 1, 1, 3, 2, 4],
            [0, 2, 3, 1, 1, 3, 2, 5],
            [0, 3, 1, 3, 3, 1, 3, 6],
            [0, 1, 3, 2, 2, 3, 1, 7]
        ]

    def get_color(self, row, col):
        # Retorna o código numérico da cor na coordenada especificada
        return self.grid[row][col]