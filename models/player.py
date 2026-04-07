class Player:
    def __init__(self, name):
        # Define o nome, fichas iniciais e histórico de apostas
        self.name = name
        self.chips = 15
        self.rounds_played = 0
        self.bets = {
            'quadrant': 0,
            'red': 0,
            'green': 0,
            'blue': 0,
            'ordered_pair': 0
        }

    def place_bet(self, bet_type, amount):
        # Subtrai o valor da aposta se houver fichas suficientes
        if self.chips >= amount:
            self.chips -= amount
            self.bets[bet_type] += amount
            self.rounds_played += 1
            return True
        return False

    def reset_bets(self):
        # Zera as apostas da rodada atual
        self.bets = {k: 0 for k in self.bets}

    def win_chips(self, winnings, original_bet):
        # Adiciona o prêmio e o valor apostado de volta às fichas
        self.chips += (winnings + original_bet)