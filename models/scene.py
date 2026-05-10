import pygame
from config import *

class Scene:
    def __init__(self, size):
        self.size = size
        self.offset_x = 50
        self.offset_y = 60
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 4],
            [0, 1, 3, 2, 2, 3, 1, 4],
            [0, 3, 1, 3, 3, 1, 3, 4],
            [0, 2, 3, 1, 1, 3, 2, 4],
            [0, 2, 3, 1, 1, 3, 2, 5],
            [0, 3, 1, 3, 3, 1, 3, 6],
            [0, 1, 3, 2, 2, 3, 1, 7]
        ]
        self.input_active = True
        # Caixa de input reposicionada para o painel lateral (X=870, Y=350)
        self.input_rect = pygame.Rect(910, 350, 300, 50)
        self.input_text = ''

    def paint_line(self, screen, number_line, line):
        edge_radius = 8 
        color_grid = (226, 232, 240) 
        
        for number_col, house_board in enumerate(line):
            x = (number_col * self.size) + self.offset_x
            y = (number_line * self.size) + self.offset_y
            
            # --- 1. DESENHA O GRID DE FUNDO ---
            if number_col < len(line) - 1:
                pygame.draw.rect(screen, WHITE, (x, y, self.size, self.size))
                pygame.draw.rect(screen, color_grid, (x, y, self.size, self.size), 1)

            # --- 2. DESENHA O NÚMERO DA LINHA (Coluna 0) ---
            if house_board == 0 and number_col == 0:
                font = pygame.font.SysFont('segoeui', 36, bold=True)
                text = font.render(str(number_line), True, TEXT_COLOR)
                
                # Calcula o centro horizontal e vertical da célula (self.size)
                text_x = x + (self.size // 2) - (text.get_width() // 2)
                text_y = y + (self.size // 2) - (text.get_height() // 2)
                
                screen.blit(text, (text_x, text_y))
                continue
            
            # --- 3. DESENHA AS PEÇAS ---
            if house_board in (1, 2, 3):
                color_item = RED if house_board == 1 else GREEN if house_board == 2 else BLUE
                pygame.draw.rect(screen, SHADOW, (x + 4, y + 4, self.size - 8, self.size - 8), border_radius=edge_radius)
                pygame.draw.rect(screen, color_item, (x + 2, y + 2, self.size - 8, self.size - 8), border_radius=edge_radius)
                
                font = pygame.font.SysFont('segoeui', 30, bold=True)
                if number_line == 2 and number_col == 5:
                    text = font.render("Q" + str(number_line-1), True, WHITE)
                    screen.blit(text, (x + 25, y + self.size // 2 - 15))
                if number_line == 2 and number_col == 2:
                    text = font.render("Q" + str(number_line), True, WHITE)
                    screen.blit(text, (x + 25, y + self.size // 2 - 15))
                if number_line == 5 and number_col == 2:
                    text = font.render("Q" + str(number_line-2), True, WHITE)
                    screen.blit(text, (x + 25, y + self.size // 2 - 15))
                if number_line == 5 and number_col == 5:
                    text = font.render("Q" + str(number_line-1), True, WHITE)
                    screen.blit(text, (x + 25, y + self.size // 2 - 15))

            # --- 4. DESENHA OS BOTÕES LATERAIS DO board ---
            if house_board in (4, 5, 6, 7):
                width_button = self.size + 100
                color_button = WHITE
                if house_board == 5: color_button = BLUE
                elif house_board == 6: color_button = RED
                elif house_board == 7: color_button = GREEN

                pygame.draw.rect(screen, SHADOW, (x + 4, y + 4, width_button, self.size - 10), border_radius=edge_radius)
                pygame.draw.rect(screen, color_button, (x, y, width_button, self.size - 10), border_radius=edge_radius)
                
                if house_board == 4:
                    pygame.draw.rect(screen, (203, 213, 225), (x, y, width_button, self.size - 10), 2, border_radius=edge_radius)
                
                font = pygame.font.SysFont('segoeui', 32, bold=True)
                text_color = TEXT_COLOR if house_board == 4 else WHITE
                
                text = ""
                if house_board == 4: text = f"Quad {number_line + 1}"
                elif house_board == 5: text = "blue"
                elif house_board == 6: text = "red"
                elif house_board == 7: text = "green"
                
                text_render = font.render(text, True, text_color)
                screen.blit(text_render, (x + 15, y + self.size // 2 - 15))

    def draw_column_numbers(self, screen):
        font = pygame.font.SysFont('segoeui', 36, bold=True)
        for i in range(1, len(self.board[0]) - 1):
            # Adiciona o offset_x aqui também
            x = (i * self.size) + self.offset_x
            text = font.render(str(i), True, TEXT_COLOR)
            # O y (topo) ganha um pequeno ajuste de margem
            screen.blit(text, (x + self.size // 2 - 10, self.offset_y + 20))

    def paint_board(self, screen):
        for number_line, line in enumerate(self.board):
            self.paint_line(screen, number_line, line)
        self.draw_column_numbers(screen) 

    def check_click(self, pos):
        mouse_x, mouse_y = pos
        for number_line, line in enumerate(self.board):
            for number_col, house_board in enumerate(line):
                # O clique TAMBÉM precisa considerar o deslocamento!
                x = (number_col * self.size) + self.offset_x
                y = (number_line * self.size) + self.offset_y
                
                if x < mouse_x < x + self.size + 120 and y < mouse_y < y + self.size:
                    if house_board in (4, 5, 6, 7):
                        return house_board, number_col, number_line
                
                if number_line == 0 or number_col == 0:
                    continue
                
                if x < mouse_x < x + self.size and y < mouse_y < y + self.size:
                    if house_board in (1, 2, 3):
                        return house_board, number_col, number_line
        return None

    def toggle_input(self):
        self.input_active = not self.input_active
        self.input_text = ''