import pygame

class GameMessageView:
    def __init__(self, screen_width, screen_height):
        # Configura as posições para as mensagens do jogo
        self.width = screen_width
        self.height = screen_height
        self.font = pygame.font.SysFont(None, 30)
        self.black = (0, 0, 0)

    def draw(self, surface, message):
        # Renderiza o texto de feedback (ganhou/perdeu)
        text_surface = self.font.render(message, True, self.black)
        surface.blit(text_surface, (self.width - 470, self.height - 680))


class ScoreBoardView:
    def __init__(self, screen_height):
        # Responsável apenas por mostrar os nomes e fichas
        self.height = screen_height
        self.font = pygame.font.SysFont(None, 45)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

    def draw(self, surface, players):
        # Desenha os status de cada jogador em loop
        for idx, player in enumerate(players):
            color = self.blue if idx == 0 else self.red
            name_text = self.font.render(f"{player.name}:", True, color)
            chips_text = self.font.render(f" {player.chips} fichas", True, self.black)
            
            y_pos = self.height - 100 + (idx * 40)
            surface.blit(name_text, (20, y_pos))
            surface.blit(chips_text, (20 + name_text.get_width(), y_pos))


class BetInputView:
    def __init__(self, screen_width, screen_height):
        # Responsável pelo campo onde o usuário digita a aposta
        self.width = screen_width
        self.height = screen_height
        self.font_small = pygame.font.SysFont(None, 30)
        self.font_medium = pygame.font.SysFont(None, 40)
        self.black = (0, 0, 0)

    def draw(self, surface, input_text, input_rect):
        # Desenha a label e o retângulo de input
        label = self.font_small.render("Sua aposta aparece aqui:", True, self.black)
        surface.blit(label, (self.width - 370, self.height - 425))
        
        pygame.draw.rect(surface, self.black, input_rect, 2)
        input_surface = self.font_medium.render(input_text, True, self.black)
        surface.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))