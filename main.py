"""
Main game module - entry point and game loop.
"""

import pygame
import os
import sys
from logic import *
from settings import MAX_LEVEL, MAX_COLORS, WIDTH, HEIGHT
from graphics import *
from game_state import GameState
from save_data import load_data, save_data


def main():
    """
    Main game loop.
    
    Handles all events, state changes, and rendering.
    Runs until player closes window.
    """
    gs = GameState()
    
    grid = None
    num_colors = 3
    running = True
    in_menu = True
    in_stats = False
    in_settings = False
    game_complete = False
    
    # button references
    start_btn = None
    stats_btn = None
    settings_btn = None
    window_btn = None
    reset_btn = None
    color_btns = []
    
    run_total = 0
    run_best = 0
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if in_stats or in_settings:
                        in_stats = False
                        in_settings = False
                        in_menu = True
                    elif not in_menu:
                        in_menu = True
                        game_complete = False
                
                # next level shortcut
                if event.key == pygame.K_RETURN:
                    if not in_menu and not game_complete and not in_stats and not in_settings:
                        if gs.level >= MAX_LEVEL:
                            run_total += gs.score
                            gs.next_level()
                            gs.level = MAX_LEVEL
                            game_complete = True
                        else:
                            if gs.score > run_best:
                                run_best = gs.score
                            run_total += gs.score
                            gs.next_level()
                            grid, _, _ = generate_level(gs.level)
                            num_colors = min(3 + ((gs.level - 1) // 3), MAX_COLORS)
                
                # toggle color power
                if event.key == pygame.K_c and not in_menu and not game_complete:
                    gs.toggle_color_mode()

            # mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # menu clicks
                if in_menu:
                    if start_btn and start_btn.collidepoint(mpos):
                        gs.reset()
                        run_total = 0
                        run_best = 0
                        grid, _, _ = generate_level(gs.level)
                        num_colors = min(3 + ((gs.level - 1) // 3), MAX_COLORS)
                        in_menu = False
                        game_complete = False
                    elif stats_btn and stats_btn.collidepoint(mpos):
                        in_menu = False
                        in_stats = True
                    elif settings_btn and settings_btn.collidepoint(mpos):
                        in_menu = False
                        in_settings = True
                    continue
                
                # settings clicks
                if in_settings:
                    if window_btn and window_btn.collidepoint(mpos):
                        gs.save_data["settings"]["large_window"] = not gs.save_data["settings"]["large_window"]
                        save_data(gs.save_data)
                        # need restart for window change
                        pygame.quit()
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    elif reset_btn and reset_btn.collidepoint(mpos):
                        # wipe all stats
                        gs.save_data["high_score"] = 0
                        gs.save_data["total_bubbles_popped"] = 0
                        gs.save_data["total_games_played"] = 0
                        gs.save_data["levels_completed"] = 0
                        gs.save_data["level_high_scores"] = {}
                        gs.high_score = 0
                        save_data(gs.save_data)
                    continue
                
                if in_stats or game_complete:
                    continue
                
                # color picker clicks
                if gs.selected_bubble and color_btns:
                    for btn, color_idx in color_btns:
                        if btn.collidepoint(mpos):
                            r, c = gs.selected_bubble
                            val = grid[r][c]
                            if is_bomb(val):
                                grid[r][c] = color_idx + 8
                            else:
                                grid[r][c] = color_idx
                            gs.use_color_power()
                            continue

                # bubble clicks
                hover = get_mouse_coordinates(mpos, grid)
                
                if hover is not None:
                    r, c = hover
                    val = grid[r][c]
                    
                    # color mode selection
                    if gs.color_mode and not gs.selected_bubble:
                        if val != 0 and val != 8:
                            gs.select_bubble(r, c)
                        continue
                    
                    # bomb click
                    if is_bomb(val):
                        all_popped = []
                        bomb_queue = [(r, c)]
                        
                        # chain reaction loop
                        while bomb_queue:
                            br, bc = bomb_queue.pop(0)
                            if grid[br][bc] == 0:
                                continue
                            
                            group = pop_bomb(grid, br, bc)
                            
                            # check for chain bombs
                            for pr, pc in group:
                                if is_bomb(grid[pr][pc]) and (pr, pc) != (br, bc):
                                    if (pr, pc) not in bomb_queue:
                                        bomb_queue.append((pr, pc))
                            
                            pop_animation(grid, group, run_total + gs.score, gs)
                            
                            for pr, pc in group:
                                if (pr, pc) not in all_popped:
                                    all_popped.append((pr, pc))
                                if (pr, pc) not in bomb_queue:
                                    grid[pr][pc] = 0
                        
                        # handle floating bubbles
                        floaters = get_floating_bubbles(grid)
                        if floaters:
                            falling_animation(grid, floaters, max(run_best, gs.score), gs)
                            remove_floating_bubbles(grid, floaters)
                        
                        gs.add_score(len(all_popped), len(floaters))
                        if gs.score > run_best:
                            run_best = gs.score
                        continue
                    
                    # regular bubble click
                    group = get_connected_bubbles(grid, r, c)
                    if len(group) >= 3:
                        orig_color = get_color(val)
                        
                        pop_animation(grid, group, max(run_best, gs.score), gs)
                        pop_bubbles(grid, group)
                        
                        # create bomb if big group
                        if len(group) >= 6 and orig_color > 0:
                            grid[r][c] = orig_color + 8

                        floaters = get_floating_bubbles(grid)
                        if floaters:
                            falling_animation(grid, floaters, max(run_best, gs.score), gs)
                            remove_floating_bubbles(grid, floaters)

                        gs.add_score(len(group), len(floaters))
                        if gs.score > run_best:
                            run_best = gs.score

        # rendering
        if in_menu:
            start_btn, stats_btn, settings_btn = draw_menu(mpos)
        elif in_stats:
            draw_stats(gs.get_stats())
        elif in_settings:
            window_btn, reset_btn = draw_settings(gs.save_data["settings"], mpos)
        elif game_complete:
            draw_game_complete(run_best)
        else:
            hover = get_mouse_coordinates(mpos, grid)
            draw_window(grid, hover)
            draw_ui(gs, max(run_best, gs.score))
            
            if gs.selected_bubble:
                color_btns = draw_color_picker(num_colors, gs.selected_bubble)
            else:
                color_btns = []
            
            pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()