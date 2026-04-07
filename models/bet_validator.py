class BetValidator:
    # Dicionário mapeando o índice do quadrante para os intervalos válidos (range_dice1, range_dice2)
    QUADRANT_RULES = {
        0: (range(1, 4), range(4, 7)),
        1: (range(1, 4), range(1, 4)),
        2: (range(4, 7), range(1, 4)),
        3: (range(4, 7), range(4, 7))
    }

    # Mapeamento do botão clicado para o código da cor no tabuleiro
    COLOR_RULES = {
        5: 3,  # Botão 5 -> Cor 3 (Azul)
        6: 1,  # Botão 6 -> Cor 1 (Vermelho)
        7: 2   # Botão 7 -> Cor 2 (Verde)
    }

    @classmethod
    def evaluate_quadrant(cls, quadrant_index, dice1, dice2):
        # Retorna tuplas vazias por padrão caso o índice seja inválido, evitando quebras
        valid_range1, valid_range2 = cls.QUADRANT_RULES.get(quadrant_index, ([], []))
        
        # Avalia imediatamente se os dados estão dentro dos intervalos matemáticos
        return dice1 in valid_range1 and dice2 in valid_range2

    @classmethod
    def evaluate_color(cls, bet_button_type, rolled_color):
        # Verifica se a cor sorteada corresponde à cor do botão apostado
        return cls.COLOR_RULES.get(bet_button_type) == rolled_color

    @staticmethod
    def evaluate_ordered_pair(bet_row, bet_col, dice1, dice2):
        # Verifica se a coordenada apostada bate exatamente com os dados lançados
        return bet_row == dice1 and bet_col == dice2