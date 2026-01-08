#This is the main file that runs the game loop

import pygame
import time
import math
import random
from logic import *
from settings import MAX_LEVEL, MAX_COLORS
from graphics import *
from game_state import GameState

def main():
    game_state = GameState()
    grid = None
    num_colors = 3
    run = True
    in_menu = True
    game_complete = False
    start_button = None
    color_buttons = []
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
                        num_colors = min(3 + ((game_state.level - 1) // 3), MAX_COLORS)
                
                if event.key == pygame.K_c and not in_menu and not game_complete:
                    game_state.toggle_color_mode()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if in_menu:
                    if start_button and start_button.collidepoint(mouse_pos):
                        game_state.reset()
                        grid, _, _ = generate_level(game_state.level)
                        num_colors = min(3 + ((game_state.level - 1) // 3), MAX_COLORS)
                        in_menu = False
                        game_complete = False
                    continue

                if game_complete:
                    continue
                
                if game_state.selected_bubble and color_buttons:
                    for btn_rect, color_idx in color_buttons:
                        if btn_rect.collidepoint(mouse_pos):
                            row, col = game_state.selected_bubble
                            value = grid[row][col]
                            if is_bomb(value):
                                grid[row][col] = color_idx + 8
                            else:
                                grid[row][col] = color_idx
                            game_state.use_color_power()
                            continue

                hovered_bubble = get_mouse_coordinates(mouse_pos, grid)
                
                if hovered_bubble is not None:
                    row, col = hovered_bubble
                    value = grid[row][col]
                    
                    if game_state.color_mode and not game_state.selected_bubble:
                        if value != 0 and value != 8:
                            game_state.select_bubble(row, col)
                        continue
                    
                    if is_bomb(value):
                        all_popped = []
                        bombs_to_pop = [(row, col)]
                        
                        while bombs_to_pop:
                            br, bc = bombs_to_pop.pop(0)
                            if grid[br][bc] == 0:
                                continue
                            group = pop_bomb(grid, br, bc)
                            pop_animation(grid, group, game_state)
                            
                            for r, c in group:
                                if is_bomb(grid[r][c]) and (r, c) != (br, bc):
                                    bombs_to_pop.append((r, c))
                                all_popped.append((r, c))
                                grid[r][c] = 0
                        
                        floating = get_floating_bubbles(grid)
                        floating_count = len(floating)
                        if floating:
                            falling_animation(grid, floating, game_state)
                            remove_floating_bubbles(grid, floating)
                        
                        game_state.add_score(len(all_popped), floating_count)
                        continue
                    
                    group = get_connected_bubbles(grid, row, col)
                    if len(group) >= 3:
                        original_color = get_color(value)
                        
                        pop_animation(grid, group, game_state)
                        pop_bubbles(grid, group)
                        
                        if len(group) >= 6 and original_color > 0:
                            grid[row][col] = original_color + 8

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
            
            if game_state.selected_bubble:
                color_buttons = draw_color_picker(num_colors, game_state.selected_bubble)
            else:
                color_buttons = []
            
            pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()