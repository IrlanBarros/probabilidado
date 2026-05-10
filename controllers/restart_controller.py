from models.player import Player

class RestartController:
    @staticmethod
    def restart_game(game):
        game.game_started = False
        players_names = game.request_names()
        game.players = [Player(players_names[0]), Player(players_names[1])]
        game.current_player = 0
        game.current_round = 1
        game.game_message = "Seja bem vindo ao Probabilidado!"
        game.roll_dice()
        game.tie = False
        game.game_over = False