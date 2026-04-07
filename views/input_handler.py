import pygame

class InputHandler:
    def __init__(self, cell_size):
        # Armazena o tamanho da célula para calcular a posição na matriz
        self.cell_size = cell_size

    def get_grid_position(self, mouse_pos):
        # Converte as coordenadas do mouse em pixels (x, y) para índices (linha, coluna)
        mouse_x, mouse_y = mouse_pos
        
        col = mouse_x // self.cell_size
        row = mouse_y // self.cell_size
        
        return row, col

    def handle_keyboard_input(self, event, current_text):
        # Trata os eventos de teclado para a caixa de aposta (apenas números e backspace)
        if event.key == pygame.K_BACKSPACE:
            return current_text[:-1]
        
        # event.unicode pega o caractere exato que foi digitado
        elif event.unicode.isdigit():
            return current_text + event.unicode
            
        return current_text