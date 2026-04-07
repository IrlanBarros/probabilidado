import pygame

class AxisLabelRenderer:
    def __init__(self, cell_size):
        # Desenha apenas os números indicadores de linha e coluna
        self.cell_size = cell_size
        self.font = pygame.font.SysFont(None, 40)
        self.black = (0, 0, 0)

    def draw_row_number(self, surface, row_idx, x, y):
        # Desenha o número da linha na primeira coluna
        text = self.font.render(str(row_idx), True, self.black)
        surface.blit(text, (x + 25, y + self.cell_size // 2 - 10))
        pygame.draw.rect(surface, self.black, (x, y, self.cell_size + 120, self.cell_size), 1)

    def draw_column_numbers(self, surface, num_cols):
        # Desenha os números das colunas no topo
        for i in range(1, num_cols - 1):
            x = i * self.cell_size
            text = self.font.render(str(i), True, self.black)
            surface.blit(text, (x + self.cell_size // 2 - 10, 30))


class ActionPanelRenderer:
    def __init__(self, cell_size):
        # Cuida exclusivamente da coluna de botões clicáveis
        self.cell_size = cell_size
        self.font = pygame.font.SysFont(None, 40)
        self.black = (0, 0, 0)
        
        # Dicionário de despacho para remover a estrutura if/elif
        # Chave: valor da célula -> Valor: dict com propriedades visuais
        self.button_configs = {
            5: {"label": "Azul", "bg_color": (0, 0, 255), "text_color": self.black},
            6: {"label": "Vermelho", "bg_color": (255, 0, 0), "text_color": self.black},
            7: {"label": "Verde", "bg_color": (0, 255, 0), "text_color": self.black}
        }

    def draw_button(self, surface, cell_value, row_idx, x, y):
        # Recupera as configurações do botão em O(1) usando o dicionário
        config = self.button_configs.get(cell_value)
        
        # O botão do quadrante é dinâmico, então montamos ele aqui
        if cell_value == 4:
            config = {"label": f"Q{row_idx + 1}", "bg_color": (255, 255, 255), "text_color": self.black}
            
        if not config:
            return

        # Renderiza a caixa do botão com as cores mapeadas
        pygame.draw.rect(surface, config["bg_color"], (x, y, self.cell_size + 120, self.cell_size))
        pygame.draw.rect(surface, self.black, (x, y, self.cell_size + 120, self.cell_size), 1)
        
        # Renderiza o texto do botão
        text = self.font.render(config["label"], True, config["text_color"])
        surface.blit(text, (x + 25, y + self.cell_size // 2 - 10))


class GridRenderer:
    def __init__(self, cell_size):
        # Renderiza as células comuns do tabuleiro (onde os dados caem)
        self.cell_size = cell_size
        self.black = (0, 0, 0)
        
        # Mapeamento direto de valor para cor
        self.color_map = {
            1: (255, 0, 0),  # Vermelho
            2: (0, 255, 0),  # Verde
            3: (0, 0, 255)   # Azul
        }

    def draw_colored_cell(self, surface, cell_value, x, y):
        # Busca a cor direto no mapa; se não achar, não desenha
        color = self.color_map.get(cell_value)
        if color:
            pygame.draw.rect(surface, color, (x, y, self.cell_size, self.cell_size))
            pygame.draw.rect(surface, self.black, (x, y, self.cell_size, self.cell_size), 1)


class CompleteBoardView:
    def __init__(self, cell_size):
        # Instancia os subcomponentes de visualização
        self.cell_size = cell_size
        self.grid_renderer = GridRenderer(cell_size)
        self.action_panel_renderer = ActionPanelRenderer(cell_size)
        self.axis_label_renderer = AxisLabelRenderer(cell_size)
        
        # Dicionário de despacho para mapear o valor da célula ao método correspondente
        self.render_dispatch = {
            0: self._render_axis,
            1: self._render_grid,
            2: self._render_grid,
            3: self._render_grid,
            4: self._render_action,
            5: self._render_action,
            6: self._render_action,
            7: self._render_action
        }

    def _render_axis(self, surface, cell_value, row_idx, col_idx, x, y):
        # Garante que o número da linha só seja desenhado na primeira coluna
        if col_idx == 0:
            self.axis_label_renderer.draw_row_number(surface, row_idx, x, y)

    def _render_grid(self, surface, cell_value, row_idx, col_idx, x, y):
        # Renderiza células coloridas do tabuleiro
        self.grid_renderer.draw_colored_cell(surface, cell_value, x, y)

    def _render_action(self, surface, cell_value, row_idx, col_idx, x, y):
        # Renderiza os botões de ação lateral
        self.action_panel_renderer.draw_button(surface, cell_value, row_idx, x, y)

    def draw(self, surface, board_grid):
        # Delega a responsabilidade iterando sobre a matriz
        for row_idx, row in enumerate(board_grid):
            for col_idx, cell_value in enumerate(row):
                x = col_idx * self.cell_size
                y = row_idx * self.cell_size
                
                # Recupera a função de renderização em O(1) e a executa
                render_action = self.render_dispatch.get(cell_value)
                if render_action:
                    render_action(surface, cell_value, row_idx, col_idx, x, y)

        # Desenha a numeração das colunas no topo por último
        self.axis_label_renderer.draw_column_numbers(surface, len(board_grid[0]))