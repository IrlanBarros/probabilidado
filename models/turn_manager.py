class TurnManager:
    def __init__(self, players, max_rounds=5):
        # Recebe a lista de jogadores e o limite de rodadas
        self.players = players
        self.max_rounds = max_rounds
        self.current_player_index = 0
        self.current_round = 1
        self.is_finished = False
        self.winner = None
        self.is_tie = False

    def get_current_player(self):
        # Retorna o jogador que deve jogar agora
        return self.players[self.current_player_index]

    def advance_turn(self):
        # Passa a vez para o próximo jogador
        self.current_player_index = 1 if self.current_player_index == 0 else 0
        
        # Se voltou para o jogador 0, uma rodada inteira se passou
        if self.current_player_index == 0:
            self.current_round += 1
            
        self._evaluate_game_over()

    def _evaluate_game_over(self):
        # Verifica se alguém faliu ou se atingiu o limite de rodadas
        player1_bankrupt = self.players[0].chips <= 0
        player2_bankrupt = self.players[1].chips <= 0
        
        if self.current_round > self.max_rounds or player1_bankrupt or player2_bankrupt:
            self.is_finished = True
            self._determine_winner()

    def _determine_winner(self):
        # Define quem ganhou baseado na quantidade de fichas
        player1 = self.players[0]
        player2 = self.players[1]

        if player1.chips > player2.chips:
            self.winner = player1
        elif player2.chips > player1.chips:
            self.winner = player2
        else:
            self.is_tie = True