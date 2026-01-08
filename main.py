import pygame
import time
import math
import random
from logic import *
from settings import *
from graphics import *
from game_state import GameState



MAX_LEVEL = 20

def main():
    game_state = GameState()
    grid = None
    run = True
    in_menu = True
    game_complete = False
    start_button = None
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True
                    game_complete = False
                    game_state.reset()
                
                if event.key == pygame.K_RETURN and not in_menu and not game_complete:
                    if game_state.level >= MAX_LEVEL:
                        game_complete = True
                    else:
                        game_state.next_level()
                        grid, _, _ = generate_level(game_state.level)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if in_menu:
                    if start_button and start_button.collidepoint(mouse_pos):
                        game_state.reset()
                        grid, _, _ = generate_level(game_state.level)
                        in_menu = False
                        game_complete = False
                    continue

                if game_complete:
                    continue

                hovered_bubble = get_mouse_coordinates(mouse_pos, grid)
                
                if hovered_bubble is not None:
                    row, col = hovered_bubble

                    group = get_connected_bubbles(grid, row, col)
                    if len(group) >= 3:
                        pop_animation(grid, group, game_state)
                        pop_bubbles(grid, group)

                        floating = get_floating_bubbles(grid)
                        floating_count = len(floating)
                        if floating:
                            falling_animation(grid, floating, game_state)
                            remove_floating_bubbles(grid, floating)

                        game_state.add_score(len(group), floating_count)

        if in_menu:
            start_button = draw_menu(game_state.high_score)
        elif game_complete:
            draw_game_complete(game_state)
        else:
            mouse_pos = pygame.mouse.get_pos()
            hovered_bubble = get_mouse_coordinates(mouse_pos, grid)
            draw_window(grid, hovered_bubble)
            draw_ui(game_state)
            pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()