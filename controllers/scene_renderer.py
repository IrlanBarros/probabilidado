import pygame

class SceneRenderer:
    def __init__(self, width, height, board_view, score_view, message_view, bet_input_view):
        # Armazena as views e dimensões da tela
        self.width = width
        self.height = height
        self.board_view = board_view
        self.score_view = score_view
        self.message_view = message_view
        self.bet_input_view = bet_input_view
        self.input_rect = pygame.Rect(width - 350, height - 400, 200, 50)

    def draw_start_screen(self, surface):
        # Renderiza a tela inicial
        surface.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 48)
        text = font.render("Pressione ENTER para começar.", True, (0, 0, 0))
        surface.blit(text, (self.width // 2 - 250, self.height // 2))

    def draw_game_over_screen(self, surface, turn_manager):
        # Renderiza a tela de fim de jogo
        surface.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 60)
        msg = "O jogo empatou!" if turn_manager.is_tie else f"{turn_manager.winner.name} venceu!"
        text = font.render(msg + " (R para Reiniciar, S para Sair)", True, (0, 0, 0))
        surface.blit(text, (100, self.height // 2))

    def draw_active_game(self, surface, board_model, players, turn_manager, bet_manager):
        # Renderiza o jogo rodando
        surface.fill((255, 255, 255))
        
        self.board_view.draw(surface, board_model.grid)
        self.score_view.draw(surface, players)
        self.message_view.draw(surface, bet_manager.last_message)
        
        # Indicador de turno
        current_player = turn_manager.get_current_player()
        font_turn = pygame.font.SysFont(None, 45)
        color = (0, 0, 255) if turn_manager.current_player_index == 0 else (255, 0, 0)
        turn_text = font_turn.render(f"Vez do {current_player.name}", True, color)
        surface.blit(turn_text, (self.width - 460, self.height - 300))

        # Caixa de input se estiver ativa
        if bet_manager.is_active:
            self.bet_input_view.draw(surface, bet_manager.current_text, self.input_rect)