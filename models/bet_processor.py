class BetProcessor:
    def __init__(self, board_model, dice):
        # Inicializa com as dependências do tabuleiro lógico e dos dados
        self.board_model = board_model
        self.dice = dice

    def process_bet(self, player, bet_type, amount, target_value):
        # Tenta debitar a aposta do jogador
        if not player.place_bet(bet_type, amount):
            return False, "Fichas insuficientes."

        # Rola os dados para avaliar a aposta atual
        dice1, dice2 = self.dice.roll()
        is_winner = False
        winnings = 0

        # Avalia qual foi o tipo de aposta e usa o validador
        if bet_type == 'quadrant':
            is_winner = BetValidator.evaluate_quadrant(target_value, dice1, dice2)
            if is_winner:
                winnings = amount * 3
                
        elif bet_type == 'color':
            rolled_color = self.board_model.get_color(dice1, dice2)
            is_winner = BetValidator.evaluate_color(target_value, rolled_color)
            if is_winner:
                multipliers = {5: 1, 6: 2, 7: 4}
                winnings = amount * multipliers.get(target_value, 1)

        elif bet_type == 'ordered_pair':
            target_row, target_col = target_value
            is_winner = BetValidator.evaluate_ordered_pair(target_row, target_col, dice1, dice2)
            if is_winner:
                winnings = amount * 5

        # Paga o jogador em caso de vitória
        if is_winner:
            player.win_chips(winnings, amount)
            return True, f"Acertou! Ganhou {winnings} fichas."
            
        return True, "Errou a aposta."