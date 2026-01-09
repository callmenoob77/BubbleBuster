#This is the main file that runs the game loop

import pygame
import os
import sys
from logic import *
from settings import MAX_LEVEL, MAX_COLORS, WIDTH, HEIGHT
from graphics import *
from game_state import GameState
from save_data import load_data, save_data

def main():
    game_state = GameState()
    
    grid = None
    num_colors = 3
    run = True
    in_menu = True
    in_stats = False
    in_settings = False
    game_complete = False
    start_button = None
    stats_button = None
    settings_button = None
    window_button = None
    reset_button = None
    color_buttons = []
    run_total = 0
    run_best = 0
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if in_stats or in_settings:
                        in_stats = False
                        in_settings = False
                        in_menu = True
                    elif not in_menu:
                        in_menu = True
                        game_complete = False
                
                if event.key == pygame.K_RETURN and not in_menu and not game_complete and not in_stats and not in_settings:
                    if game_state.level >= MAX_LEVEL:
                        run_total += game_state.score
                        game_state.next_level()
                        game_state.level = MAX_LEVEL
                        game_complete = True
                    else:
                        if game_state.score > run_best:
                            run_best = game_state.score
                        run_total += game_state.score
                        game_state.next_level()
                        grid, _, _ = generate_level(game_state.level)
                        num_colors = min(3 + ((game_state.level - 1) // 3), MAX_COLORS)
                
                if event.key == pygame.K_c and not in_menu and not game_complete:
                    game_state.toggle_color_mode()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    if start_button and start_button.collidepoint(mouse_pos):
                        game_state.reset()
                        run_total = 0
                        run_best = 0
                        grid, _, _ = generate_level(game_state.level)
                        num_colors = min(3 + ((game_state.level - 1) // 3), MAX_COLORS)
                        in_menu = False
                        game_complete = False
                    elif stats_button and stats_button.collidepoint(mouse_pos):
                        in_menu = False
                        in_stats = True
                    elif settings_button and settings_button.collidepoint(mouse_pos):
                        in_menu = False
                        in_settings = True
                    continue
                
                if in_settings:
                    if window_button and window_button.collidepoint(mouse_pos):
                        game_state.save_data["settings"]["large_window"] = not game_state.save_data["settings"]["large_window"]
                        save_data(game_state.save_data)
                        #restart the game
                        pygame.quit()
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    elif reset_button and reset_button.collidepoint(mouse_pos):
                        #reset all statistics
                        game_state.save_data["high_score"] = 0
                        game_state.save_data["high_run_score"] = 0
                        game_state.save_data["total_bubbles_popped"] = 0
                        game_state.save_data["total_games_played"] = 0
                        game_state.save_data["levels_completed"] = 0
                        game_state.save_data["level_high_scores"] = {}
                        game_state.high_score = 0
                        save_data(game_state.save_data)
                    continue
                
                if in_stats:
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
                            
                            for r, c in group:
                                if is_bomb(grid[r][c]) and (r, c) != (br, bc):
                                    if (r, c) not in bombs_to_pop:
                                        bombs_to_pop.append((r, c))
                            
                            pop_animation(grid, group, run_total + game_state.score, game_state)
                            
                            for r, c in group:
                                if (r, c) not in all_popped:
                                    all_popped.append((r, c))
                                #don't clear bombs that are queued for explosion
                                if (r, c) not in bombs_to_pop:
                                    grid[r][c] = 0
                        
                        floating = get_floating_bubbles(grid)
                        floating_count = len(floating)
                        if floating:
                            falling_animation(grid, floating, max(run_best, game_state.score), game_state)
                            remove_floating_bubbles(grid, floating)
                        
                        game_state.add_score(len(all_popped), floating_count)
                        if game_state.score > run_best:
                            run_best = game_state.score
                        continue
                    
                    group = get_connected_bubbles(grid, row, col)
                    if len(group) >= 3:
                        original_color = get_color(value)
                        
                        pop_animation(grid, group, max(run_best, game_state.score), game_state)
                        pop_bubbles(grid, group)
                        
                        if len(group) >= 6 and original_color > 0:
                            grid[row][col] = original_color + 8

                        floating = get_floating_bubbles(grid)
                        floating_count = len(floating)
                        if floating:
                            falling_animation(grid, floating, max(run_best, game_state.score), game_state)
                            remove_floating_bubbles(grid, floating)

                        game_state.add_score(len(group), floating_count)
                        if game_state.score > run_best:
                            run_best = game_state.score

        if in_menu:
            start_button, stats_button, settings_button = draw_menu(mouse_pos)
        elif in_stats:
            draw_stats(game_state.get_stats())
        elif in_settings:
            window_button, reset_button = draw_settings(game_state.save_data["settings"], mouse_pos)
        elif game_complete:
            draw_game_complete(run_best)
        else:
            hovered_bubble = get_mouse_coordinates(mouse_pos, grid)
            draw_window(grid, hovered_bubble)
            draw_ui(game_state, max(run_best, game_state.score))
            
            if game_state.selected_bubble:
                color_buttons = draw_color_picker(num_colors, game_state.selected_bubble)
            else:
                color_buttons = []
            
            pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()