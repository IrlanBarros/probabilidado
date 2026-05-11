class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 15  # Cada jogador começa com 15 chips
        self.bets = {
            'quadrant': 0, 
            'red': 0,
            'green': 0, 
            'blue': 0, 
            'by_order': 0
        }
        self.number_rounds = 0

    def place_bet(self, type, amount):
        # print(f"bet de {amount} chips")
        self.chips -= amount
        self.bets[type] += amount
        self.number_rounds += 1

    def reset_bets(self):
        self.bets = {
            'quadrant': 0, 
            'red': 0,
            'green': 0, 
            'blue': 0, 
            'by_order': 0
        }

    def earn_chips(self, gain, bet):
        self.chips = self.chips + gain + bet
        # print(f"{self.name} Ganhou {gain} chips. chips atuais: {self.chips}")