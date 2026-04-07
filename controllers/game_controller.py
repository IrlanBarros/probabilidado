import pygame
import sys

import pygame
import sys

# Importações da Camada de Domínio (Models)
from models.player import Player
from models.dice import Dice
from models.board_model import BoardModel
from models.turn_manager import TurnManager
from models.bet_processor import BetProcessor

# Importações da Camada de Apresentação (Views)
from views.board_view import CompleteBoardView
from views.ui_view import GameMessageView, ScoreBoardView, BetInputView
from views.input_handler import InputHandler

# Importações de Componentes do Controller
from controllers.bet_input_manager import BetInputManager
from controllers.scene_renderer import SceneRenderer

# Importação do Estado Inicial (Pattern State)
from states.game_states import StartState

class GameController:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Probabilidado")
        
        self.is_running = True
        
        # Inicializa o core do jogo
        self._initialize_dependencies()
        
        # Define o estado inicial da máquina de estados
        self.current_state = StartState(self)

    def _initialize_dependencies(self):
        # Agrupa a instanciação de Models, Views e Managers
        self.players = [Player("Jogador 1"), Player("Jogador 2")]
        self.board_model = BoardModel()
        self.dice = Dice()
        self.turn_manager = TurnManager(self.players, max_rounds=5)
        self.bet_processor = BetProcessor(self.board_model, self.dice)
        
        cell_size = 600 // 7
        self.input_handler = InputHandler(cell_size)
        self.bet_manager = BetInputManager(self.bet_processor, self.turn_manager, self.input_handler)
        
        # Inicializa as Views
        board_view = CompleteBoardView(cell_size)
        score_view = ScoreBoardView(self.height)
        message_view = GameMessageView(self.width, self.height)
        bet_input_view = BetInputView(self.width, self.height)
        self.scene_renderer = SceneRenderer(
            self.width, self.height, board_view, score_view, message_view, bet_input_view
        )

    def change_state(self, new_state):
        # Altera o estado atual (ex: de StartState para PlayingState)
        self.current_state = new_state

    def reset_game(self):
        # Recria as instâncias para uma nova partida
        self._initialize_dependencies()

    def handle_events(self):
        # O Controller apenas intercepta o botão de fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            else:
                # Delega qualquer outro evento para o estado atual resolver
                self.current_state.handle_event(event)

    def render(self):
        # Delega a renderização para o estado atual e atualiza a tela
        self.current_state.render(self.screen)
        pygame.display.flip()

    def run(self):
        # O laço principal fica o mais limpo possível
        while self.is_running:
            self.handle_events()
            self.render()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameController()
    game.run()