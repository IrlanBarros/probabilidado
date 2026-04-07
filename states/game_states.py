from abc import ABC, abstractmethod
import pygame

class GameState(ABC):
    def __init__(self, context):
        # Recebe a instância do GameController para manipular o fluxo
        self.context = context

    @abstractmethod
    def handle_event(self, event):
        # Cada estado decide como lidar com os inputs do Pygame
        pass

    @abstractmethod
    def render(self, surface):
        # Cada estado decide o que desenhar na tela
        pass


class StartState(GameState):
    def handle_event(self, event):
        # Aguarda apenas a tecla ENTER para iniciar o jogo
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Transita para o estado de jogo ativo
            self.context.change_state(PlayingState(self.context))

    def render(self, surface):
        # Pede ao renderizador de cenas para desenhar a tela inicial
        self.context.scene_renderer.draw_start_screen(surface)


class PlayingState(GameState):
    def handle_event(self, event):
        # Verifica se o jogo acabou antes de processar qualquer jogada
        if self.context.turn_manager.is_finished:
            self.context.change_state(GameOverState(self.context))
            return

        # Captura cliques no tabuleiro
        if event.type == pygame.MOUSEBUTTONUP and not self.context.bet_manager.is_active:
            row, col = self.context.input_handler.get_grid_position(pygame.mouse.get_pos())
            try:
                cell_value = self.context.board_model.grid[row][col]
                self.context.bet_manager.prepare_bet(cell_value, row, col)
            except IndexError:
                pass 

        # Captura digitação da aposta
        elif event.type == pygame.KEYDOWN and self.context.bet_manager.is_active:
            self.context.bet_manager.process_keystroke(event)
            
            # Checa novamente se a rodada atual finalizou o jogo após a aposta
            if self.context.turn_manager.is_finished:
                self.context.change_state(GameOverState(self.context))

    def render(self, surface):
        # Desenha todos os elementos do jogo rodando
        self.context.scene_renderer.draw_active_game(
            surface, 
            self.context.board_model, 
            self.context.players, 
            self.context.turn_manager, 
            self.context.bet_manager
        )


class GameOverState(GameState):
    def handle_event(self, event):
        # Aceita apenas os comandos de reiniciar ou sair
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.context.reset_game()
                # Retorna para o estado inicial
                self.context.change_state(StartState(self.context))
            elif event.key == pygame.K_s:
                self.context.is_running = False

    def render(self, surface):
        # Desenha a tela de vencedor ou empate
        self.context.scene_renderer.draw_game_over_screen(surface, self.context.turn_manager)