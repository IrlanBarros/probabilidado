import pygame
import sys
from config import *
from controllers.game_controller import GameController
from controllers.restart_controller import RestartController

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
    pygame.display.set_caption("Probabilidado")

    game = GameController(screen)
    game.iniciar_jogo()

    while True:
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- REGRA DE FIM DE JOGO ---
            if game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        RestartController.restart_game(game)
                    elif event.key == pygame.K_s:
                        pygame.quit()
                        sys.exit()

            # --- TELA INICIAL ---
            elif not game.game_started:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game.game_started = True

            # --- DURANTE O JOGO ---
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    game.process_current_bet(mouse_position)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        game.scene.input_text = game.scene.input_text[:-1]
                    elif event.unicode.isdigit():
                        # REGRA DE LIMITE: Máximo de 3 caracteres numéricos
                        if len(game.scene.input_text) < 3:
                            game.scene.input_text += event.unicode

        # Renderização da tela
        if game.game_over:
            game.show_winner()
            
        elif not game.game_started:
            font = pygame.font.SysFont(None, 48)
            for i, line in enumerate(RULES):
                text = font.render(line, True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 30 + i * 40))
        else:
            game.design_interface()
            if game.scene.input_active:
                pygame.draw.rect(screen, SHADOW, (game.scene.input_rect.x + 3, game.scene.input_rect.y + 3, game.scene.input_rect.width, game.scene.input_rect.height), border_radius=10)
                pygame.draw.rect(screen, WHITE, game.scene.input_rect, border_radius=10)
                pygame.draw.rect(screen, BLUE, game.scene.input_rect, 2, border_radius=10)
                
                font = pygame.font.SysFont('segoeui', 36)
                input_surface = font.render(game.scene.input_text, True, TEXT_COLOR)
                screen.blit(input_surface, (game.scene.input_rect.x + 15, game.scene.input_rect.y + 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()