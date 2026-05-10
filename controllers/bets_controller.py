class BetsController:
    def __init__(self, game):
        # Armazena a referência do GameController
        self.game = game

    def bet_input(self):
        if self.game.scene.input_text.isdigit():
            bet_amount = int(self.game.scene.input_text)
        else:
            bet_amount = 0
            
        self.game.scene.input_text = ''
        return bet_amount

    def process_bet(self, mouse_position):
        click_result = self.game.scene.check_click(mouse_position)
        if not click_result:
            return False # Clique fora, não troca o turno

        house_board, number_col, number_line = click_result
        bet = self.bet_input()
        player = self.game.players[self.game.current_player]
        print(f"número de chips: {player.chips}")

        if player.chips < bet or bet <= 0:
            self.game.game_message = f"{player.nome} não tem {bet} fichas para apostar."
            return False

        if house_board == 4:
            self.quadrant_bet(number_line, bet)
        elif house_board in (5, 6, 7):
            colors = {5: 'blue', 6: 'red', 7: 'green'}
            self.color_bet(house_board, colors[house_board], bet)
        else:
            house_position = (number_line, number_col)
            self.by_order_bet(house_position, bet)
            
        return True # aposta processada com sucesso

    def quadrant_bet(self, line, bet):
        player = self.game.players[self.game.current_player]
        player.place_bet('quadrant', bet)
        
        d1, d2 = self.game.dice1, self.game.dice2
        sure_bet = False

        if line == 0 and (0 < d1 < 4) and (3 < d2 < 7):
            sure_bet = True
        elif line == 1 and (0 < d1 < 4) and (0 < d2 < 4):
            sure_bet = True
        elif line == 2 and (3 < d1 < 7) and (0 < d2 < 4):
            sure_bet = True
        elif line == 3 and (3 < d1 < 7) and (3 < d2 < 7):
            sure_bet = True

        if sure_bet:
            player.earn_chips(bet * 3, bet)
            
            if self.game.sound_win:
                self.game.sound_win.play()
            self.game.game_message = f"Acertou, aposta no quadrante {line + 1}!!"
        else:
            if self.game.sound_loss:
                self.game.sound_loss.play()
            self.game.game_message = f"Errou! Aposta no quadrante {line + 1}.\n Dados: ({d1}, {d2})"

    def color_bet(self, house, color, bet):
        player = self.game.players[self.game.current_player]
        player.place_bet(color, bet)
        
        house_dice = self.game.scene.board[self.game.dice1][self.game.dice2]
        sure_bet = False
        multiplies = 0

        if house == 5 and house_dice == 3: # azul
            sure_bet, multiplies = True, 1
        elif house == 6 and house_dice == 1: # vermelho
            sure_bet, multiplies = True, 2
        elif house == 7 and house_dice == 2: # verde
            sure_bet, multiplies = True, 4

        if sure_bet:
            player.earn_chips(bet * multiplies, bet)
            
            if self.game.sound_win:
                self.game.sound_win.play()
            self.game.game_message = f"Acertou com aposta na cor {color}!"
        else:
            if self.game.sound_loss:
                self.game.sound_loss.play()
            self.game.game_message = f"Errou! Aposta na cor {color}.\n Dados: ({self.game.dice1}, {self.game.dice2})"

    def by_order_bet(self, house_position, bet):
        player = self.game.players[self.game.current_player]
        player.place_bet('by_order', bet)
        
        if (self.game.dice1, self.game.dice2) == house_position:
            player.earn_chips(bet * 5, bet)
            
            if self.game.sound_win:
                self.game.sound_win.play()
            self.game.game_message = "Acertou com aposta em par ordenado!"
        else:
            if self.game.sound_loss:
                self.game.sound_loss.play()
            self.game.game_message = f"Errou! Aposta em par ordenado.\n Dados: ({self.game.dice1}, {self.game.dice2})"