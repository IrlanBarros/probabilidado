import pygame
import sys
import random
import datetime
import os
from config import *
from models.player import Player
from models.scene import Scene
from controllers.bets_controller import BetsController
from controllers.restart_controller import RestartController

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.scene = Scene(600 // 7)
        self.players = []
        self.current_player = 0
        self.current_round = 1
        self.game_message = "Seja bem vindo ao Probabilidado!"
        self.game_started = False
        self.tie = False
        self.dice1 = 0
        self.dice2 = 0
        self.game_over = False
        try:
            self.sound_dice = pygame.mixer.Sound('assets/sounds/dice.wav')
            self.sound_win = pygame.mixer.Sound('assets/sounds/win.wav')
            self.sound_loss = pygame.mixer.Sound('assets/sounds/loss.wav')
            self.sound_dice.set_volume(0.5) 
            self.sound_win.set_volume(0.7)
            self.sound_loss.set_volume(0.7)
        except FileNotFoundError:
            print("Aviso: Arquivos de som não encontrados na pasta assets/sounds/")
            self.sound_dice = None
            self.sound_win = None
            self.sound_loss = None
            
        try:
            pygame.mixer.music.load('assets/music/background.ogg')
            pygame.mixer.music.set_volume(0.1) # Som em volume ambiente
            pygame.mixer.music.play(-1) # loop infinito
        except Exception:
            print("Aviso: Arquivo de música não encontrado.")
        
        # Injeta o próprio GameController no BetsController
        self.bets_controller = BetsController(self)

    def roll_dice(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        
        if self.sound_dice:
            self.sound_dice.play()
        # print(f"Dados lançados: ({self.dice1}, {self.dice2})")

    def iniciar_jogo(self):
        names = self.request_names()
        self.players = [Player(names[0]), Player(names[1])]
        self.roll_dice()

    def process_current_bet(self, mouse_position):
        valid_bet = self.bets_controller.process_bet(mouse_position)
        if valid_bet:
            self.check_game_over()
            if not self.game_over:
                self.switch_shifts()

    def switch_shifts(self):
        self.current_player = 1 if self.current_player == 0 else 0
        self.roll_dice()

    def request_names(self):
        names = []
        font = pygame.font.SysFont(None, 48)
        input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 25, 400, 50)
        
        for i in range(2):
            name = ""
            while True:
                self.screen.fill(BG_COLOR)
                text_surface = font.render(f"Insira o nome do jogador {i + 1}:", True, BLACK)
                self.screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))
                pygame.draw.rect(self.screen, BLACK, input_rect, 2)
                
                text_color = BLUE if i == 0 else RED
                input_surface = font.render(name, True, text_color)
                self.screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            names.append(name.strip() or f"Jogador {i + 1}")
                            break
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if len(name) < 12:
                                name += event.unicode
                else:
                    continue
                break
        return names

    def design_interface(self):
        self.scene.paint_board(self.screen)
        
        # --- DESENHA O PAINEL LATERAL (DASHBOARD) ---
        painel_rect = pygame.Rect(860, 50, 400, HEIGHT - 100)
        pygame.draw.rect(self.screen, SHADOW, (painel_rect.x + 8, painel_rect.y + 8, painel_rect.width, painel_rect.height), border_radius=20)
        pygame.draw.rect(self.screen, WHITE, painel_rect, border_radius=20)
        
        # Renderiza os componentes internos alinhados a este painel
        self.show_player_turn()
        self.show_message()
        self.show_bet_location()
        self.show_info_player()

    def show_player_turn(self):
        font = pygame.font.SysFont('segoeui', 36, bold=True)
        player = self.players[self.current_player]
        color = BLUE if self.current_player == 0 else RED
        
        title = font.render("TURNO ATUAL", True, TEXT_COLOR)
        name = font.render(player.name, True, color)
        
        # Centralizado no topo do painel lateral
        self.screen.blit(title, (1060 - title.get_width()//2, 80))
        self.screen.blit(name, (1060 - name.get_width()//2, 120))

    def show_message(self):
        # Quebra a mensagem se for muito longa para caber no painel
        font = pygame.font.SysFont('segoeui', 24)
        text_surface = font.render(self.game_message, True, (100, 116, 139)) # Cinza médio
        
        # Centralizado abaixo de quem é a vez
        self.screen.blit(text_surface, (1060 - text_surface.get_width()//2, 180))

    def show_bet_location(self):
        font = pygame.font.SysFont('segoeui', 26, bold=True)
        text_surface = font.render("VALOR DA APOSTA:", True, TEXT_COLOR)
        
        self.screen.blit(text_surface, (940, 310))

    def show_info_player(self):
        # Transforma o placar em "Cartões" na parte de baixo do painel
        y_base = 450
        
        for idx, player in enumerate(self.players):
            theme_color = BLUE if idx == 0 else RED
            card_rect = pygame.Rect(910, y_base + (idx * 80), 300, 60)
            
            # Fundo suave do cartão
            bg_color = (239, 246, 255) if idx == 0 else (254, 242, 242)
            pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=10)
            pygame.draw.rect(self.screen, theme_color, card_rect, 2, border_radius=10)
            
            # textos dentro do cartão
            font_name = pygame.font.SysFont('segoeui', 28, bold=True)
            font_chips = pygame.font.SysFont('segoeui', 28)
            
            text_name = font_name.render(player.name, True, theme_color)
            text_chips = font_chips.render(f"{player.chips} fichas", True, TEXT_COLOR)
            
            self.screen.blit(text_name, (card_rect.x + 15, card_rect.y + 15))
            self.screen.blit(text_chips, (card_rect.right - text_chips.get_width() - 15, card_rect.y + 15))
        
    def check_game_over(self):
        j1, j2 = self.players[0], self.players[1]
        
        # Regra 2: Morte súbita se alguém zerar as fichas
        if j1.chips <= 0 or j2.chips <= 0:
            self.game_over = True
            self.tie = False
            self.save_match_history()
            return

        # Regra 1: Fim ao término das rodadas configuradas
        if j1.number_rounds >= number_rounds and j2.number_rounds >= number_rounds:
            self.game_over = True
            self.tie = (j1.chips == j2.chips)
            self.save_match_history()

    def show_winner(self):
        font = pygame.font.SysFont(None, 60)
        
        if self.tie:
            text = f"Empate! Ambos terminaram com {self.players[0].chips} fichas."
        else:
            # Descobre quem tem mais fichas
            winner = self.players[0] if self.players[0].chips > self.players[1].chips else self.players[1]
            loser = self.players[1] if winner == self.players[0] else self.players[0]
            
            # Mensagem customizada caso o derrotado tenha zerado as fichas
            if loser.chips <= 0:
                text = f"{winner.name} venceu! {loser.name} faliu."
            else:
                text = f"Parabéns, {winner.name}! Venceu com {winner.chips} fichas!"
                
        text_winner = font.render(text, True, BLACK)
        self.screen.blit(text_winner, (WIDTH // 2 - text_winner.get_width() // 2, HEIGHT // 2 - 50))

        font_options = pygame.font.SysFont(None, 40)
        option_reiniciar = font_options.render("Pressione R para jogar novamente", True, GREEN)
        option_sair = font_options.render("Pressione S para sair", True, RED)
        self.screen.blit(option_reiniciar, (WIDTH // 2 - option_reiniciar.get_width() // 2, HEIGHT // 2 + 50))
        self.screen.blit(option_sair, (WIDTH // 2 - option_sair.get_width() // 2, HEIGHT // 2 + 100))
        
    def save_match_history(self):
        folder_name = "data"
        file_path = os.path.join(folder_name, "match_history.txt")

        # Verifica se a pasta existe, se não, cria ela
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Prepara os dados para o log
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p1, p2 = self.players[0], self.players[1]
        
        if self.tie:
            result = "Empate"
        else:
            winner = p1 if p1.chips > p2.chips else p2
            result = f"Vencedor: {winner.name}"

        log_entry = f"Partida ocorrida em [{timestamp}]: {p1.name} ({p1.chips} fichas) vs {p2.name} ({p2.chips} fichas) | {result}\n"
        
        try:
            # Agora abre o arquivo usando o caminho completo (data/match_history.txt)
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(log_entry)
            # print(f"Histórico de partidas salvo em {file_path}")
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")