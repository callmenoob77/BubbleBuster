#This is the py file for the graphics part, like the popping of the baloons and tings like that

import pygame
import math
from settings import *

#init fonts once
pygame.font.init()
FONT_TITLE = pygame.font.SysFont("Arial", 64)
FONT_BIG = pygame.font.SysFont("Arial", 48)
FONT_BUTTON = pygame.font.SysFont("Arial", 36)
FONT_TEXT = pygame.font.SysFont("Arial", 28)
FONT_SMALL = pygame.font.SysFont("Arial", 24)
FONT_TINY = pygame.font.SysFont("Arial", 20)

#Pre-create overlay to save performance
OVERLAY = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
OVERLAY.fill((0, 0, 0, 150)) #Default menu dimming
OVERLAY_DARK = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
OVERLAY_DARK.fill((0, 0, 0, 180)) #Darker for game over/level complete

#converts grid position to pixel position for drawing
def get_pixel_coordinates(row, col, grid=None):
    if grid is not None:
        num_rows = len(grid)
        num_cols = len(grid[0]) if grid else 8
        grid_start_x = (WIDTH - num_cols * diam) / 2
        grid_start_y = (HEIGHT - num_rows * diam) / 2
    else:
        grid_start_x = start_x
        grid_start_y = start_y
    
    x = grid_start_x + (col * diam)
    y = grid_start_y + (row * diam)
    
    if row % 2 == 1:
        x += radius
        
    return int(x + radius), int(y + radius)


#checks what bubble the mouse is over
def get_mouse_coordinates(mouse_pos, grid):
    mx, my = mouse_pos

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            bubble_x, bubble_y = get_pixel_coordinates(r, c, grid)
            distanta = math.sqrt((mx - bubble_x)**2 + (my - bubble_y)**2)

            if distanta < radius:
                return (r, c)
    return None


#draws all the bubbles on the screen
def draw_window(grid, hovered_bubble = None, bubbles_to_hide=[]):
    WIN.blit(BG, (0, 0))
    colors = [
        "white",
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "cyan",
        "orange"
    ]

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            value = grid[r][c]

            if (r, c) in bubbles_to_hide:
                continue
            
            if value == 0:
                continue

            pos_row, pos_col = get_pixel_coordinates(r, c, grid)
            
            if value == 8:
                pygame.draw.circle(WIN, "gray", (pos_row, pos_col), radius - 2)
                pygame.draw.circle(WIN, "darkgray", (pos_row, pos_col), radius - 2, 3)
            elif 9 <= value <= 15:
                color = colors[value - 8]
                pygame.draw.circle(WIN, color, (pos_row, pos_col), radius - 2)
                pygame.draw.circle(WIN, "white", (pos_row, pos_col), radius // 3)
            else:
                pygame.draw.circle(WIN, colors[value], (pos_row, pos_col), radius - 2)

            if hovered_bubble == (r, c):
                pygame.draw.circle(WIN, "white", (pos_row, pos_col), radius, 3)


#shrinking animation when bubbles get popped
def pop_animation(grid, group, run_total, game_state=None):
    clock = pygame.time.Clock()
    colors = [
        "white",
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "cyan",
        "orange"
    ]

    frames = 10

    for i in range(frames, 0, -1):
        clock.tick(60)

        current_radius = int(radius * (i / frames))

        draw_window(grid, hovered_bubble = None, bubbles_to_hide = group)

        if game_state:
            draw_ui(game_state, run_total)

        for r, c in group:
            value = grid[r][c]
            if value == 8:
                color = "gray"
            elif 9 <= value <= 15:
                color = colors[value - 8]
            else:
                color = colors[value]
            x, y = get_pixel_coordinates(r, c, grid)

            pygame.draw.circle(WIN, color, (x, y), current_radius)
            if i > 7:
                pygame.draw.circle(WIN, color, (x, y), current_radius, 2)
        pygame.display.update()


#falling animation when bubbles get detached from ceiling
def falling_animation(grid, floating_bubbles, run_total, game_state=None):
    clock = pygame.time.Clock()
    colors = [
        "white",
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "cyan",
        "orange"
    ]
    
    bubbles_data = []
    for r, c in floating_bubbles:
        x, y = get_pixel_coordinates(r, c, grid)
        value = grid[r][c]
        if value == 8:
            color = "gray"
        elif 9 <= value <= 15:
            color = colors[value - 8]
        else:
            color = colors[value]
        bubbles_data.append((x, y, color))
    
    frames = 30
    fall_distance = HEIGHT
    
    for frame in range(frames):
        clock.tick(60)
        offset = int((frame / frames) * fall_distance)
        
        draw_window(grid, hovered_bubble=None, bubbles_to_hide=floating_bubbles)
        
        if game_state:
            draw_ui(game_state, run_total)
        
        for x, y, color in bubbles_data:
            new_y = y + offset
            pygame.draw.circle(WIN, color, (x, new_y), radius - 2)
        
        pygame.display.update()


#Phase 4

#draws score, level, and power-ups on screen
def draw_ui(game_state, run_total):
    
    score_text = FONT_TEXT.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(score_text, (20, 20))
    
    best_text = FONT_TEXT.render(f"Best: {run_total}", True, "gold")
    WIN.blit(best_text, (20, 55))
    
    level_text = FONT_TEXT.render(f"Level: {game_state.level}", True, "white")
    WIN.blit(level_text, (WIDTH - 130, 20))
    
    hint_text = FONT_TINY.render("Press ENTER for next level  |  ESC for menu", True, "orange")
    WIN.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 40))
    
    if game_state.color_powers > 0:
        power_text = FONT_TEXT.render(f"COLOR x{game_state.color_powers} [C]", True, "cyan")
        WIN.blit(power_text, (20, 90))
    
    if game_state.color_mode and not game_state.selected_bubble:
        mode_text = FONT_TEXT.render("COLOR MODE - Click a bubble to change!", True, "yellow")
        WIN.blit(mode_text, (WIDTH//2 - mode_text.get_width()//2, 60))


#Phase 5

#draws the color picker panel when changing a bubble's color
def draw_color_picker(num_colors, selected_pos):
    colors = ["red", "blue", "green", "yellow", "purple", "cyan", "orange"]
    
    panel_width = 80
    panel_height = num_colors * 40 + 45
    panel_x = WIDTH - panel_width - 15
    panel_y = (HEIGHT - panel_height) // 2
    
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(WIN, (40, 40, 40), panel_rect, border_radius=10)
    pygame.draw.rect(WIN, "cyan", panel_rect, 3, border_radius=10)
    
    title = FONT_TINY.render("PICK", True, "cyan")
    WIN.blit(title, (panel_x + panel_width//2 - title.get_width()//2, panel_y + 8))
    
    buttons = []
    for i in range(num_colors):
        color_idx = i + 1
        btn_rect = pygame.Rect(panel_x + 15, panel_y + 35 + i * 40, 50, 30)
        
        pygame.draw.rect(WIN, colors[i], btn_rect, border_radius=5)
        pygame.draw.rect(WIN, "white", btn_rect, 2, border_radius=5)
        
        buttons.append((btn_rect, color_idx))
    
    return buttons


#shows level complete overlay
def draw_level_complete(game_state):
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    text = FONT_BIG.render("Level Complete!", True, "green")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
    
    score = FONT_TINY.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2))
    
    if game_state.score >= game_state.high_score:
        new_high = FONT_TINY.render("NEW HIGH SCORE!", True, "gold")
        WIN.blit(new_high, (WIDTH//2 - new_high.get_width()//2, HEIGHT//2 + 40))
    
    prompt = FONT_TINY.render("Click to continue...", True, "yellow")
    WIN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 90))
    
    pygame.display.update()


#shows game complete screen when you beat all levels
def draw_game_complete(run_total):
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    text = FONT_BIG.render("Good job!", True, "gold")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 120))
    
    text2 = FONT_BIG.render("You finished the game!", True, "green")
    WIN.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 50))
    
    run_score = FONT_TEXT.render(f"Best Score: {run_total}", True, "gold")
    WIN.blit(run_score, (WIDTH//2 - run_score.get_width()//2, HEIGHT//2 + 30))
    
    prompt = FONT_TEXT.render("Press ESC to get to the menu", True, "yellow")
    WIN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.update()


#draws the main menu with start button
def draw_menu(mouse_pos):
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY, (0, 0))
    
    title = FONT_TITLE.render("Bubble Buster", True, "white")
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    
    #start button with hover
    start_rect = pygame.Rect(WIDTH//2 - 120, 280, 240, 60)
    start_color = (100, 255, 100) if start_rect.collidepoint(mouse_pos) else (50, 200, 50)
    pygame.draw.rect(WIN, start_color, start_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", start_rect, 3, border_radius=10)
    btn_text = FONT_BUTTON.render("Start Game", True, "black")
    WIN.blit(btn_text, (start_rect.centerx - btn_text.get_width()//2, 
                       start_rect.centery - btn_text.get_height()//2))
    
    #stats button with hover
    stats_rect = pygame.Rect(WIDTH//2 - 120, 360, 240, 60)
    stats_color = (100, 100, 255) if stats_rect.collidepoint(mouse_pos) else (50, 50, 200)
    pygame.draw.rect(WIN, stats_color, stats_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", stats_rect, 3, border_radius=10)
    stats_text = FONT_BUTTON.render("Statistics", True, "white")
    WIN.blit(stats_text, (stats_rect.centerx - stats_text.get_width()//2, 
                         stats_rect.centery - stats_text.get_height()//2))
    
    #settings button with hover
    settings_rect = pygame.Rect(WIDTH//2 - 120, 440, 240, 60)
    settings_color = (180, 100, 200) if settings_rect.collidepoint(mouse_pos) else (128, 50, 150)
    pygame.draw.rect(WIN, settings_color, settings_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", settings_rect, 3, border_radius=10)
    settings_text = FONT_BUTTON.render("Settings", True, "white")
    WIN.blit(settings_text, (settings_rect.centerx - settings_text.get_width()//2, 
                            settings_rect.centery - settings_text.get_height()//2))
    
    instructions = FONT_TINY.render("Press ENTER to skip to the next level", True, "white")
    WIN.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 550))
    
    esc_text = FONT_TINY.render("Press ESC to return to menu", True, "gray")
    WIN.blit(esc_text, (WIDTH//2 - esc_text.get_width()//2, 580))
    
    pygame.display.update()
    return start_rect, stats_rect, settings_rect


#draws the statistics page
def draw_stats(stats):
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    title = FONT_BIG.render("Statistics", True, "cyan")
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    y = 160
    texts = [
        f"High Score: {stats['high_score']}",
        f"Total Bubbles Popped: {stats['total_bubbles']}",
        f"Games Played: {stats['games_played']}",
        f"Levels Completed: {stats['levels_completed']}"
    ]
    
    for text in texts:
        rendered = FONT_TEXT.render(text, True, "white")
        WIN.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y))
        y += 45
    
    #level high scores
    y += 20
    level_title = FONT_TEXT.render("Level High Scores:", True, "gold")
    WIN.blit(level_title, (WIDTH//2 - level_title.get_width()//2, y))
    y += 40
    
    level_scores = stats.get("level_scores", {})
    if level_scores:
        cols = 4
        col_width = 200
        start_x = WIDTH//2 - (cols * col_width)//2
        for i, (level, score) in enumerate(sorted(level_scores.items(), key=lambda x: int(x[0]))):
            col = i % cols
            row = i // cols
            x = start_x + col * col_width
            level_y = y + row * 30
            text = FONT_TINY.render(f"Level {level}: {score}", True, "white")
            WIN.blit(text, (x, level_y))
    
    back_text = FONT_TINY.render("Press ESC to go back", True, "yellow")
    WIN.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 50))
    
    pygame.display.update()


#draws the settings page
def draw_settings(settings, mouse_pos):
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    title = FONT_BIG.render("Settings", True, "purple")
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    
    #large window toggle
    window_rect = pygame.Rect(WIDTH//2 - 150, 280, 300, 60)
    window_color = "green" if settings.get("large_window", False) else "red"
    pygame.draw.rect(WIN, window_color, window_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", window_rect, 3, border_radius=10)
    window_status = "ON" if settings.get("large_window", False) else "OFF"
    window_text = FONT_TEXT.render(f"Large Window: {window_status}", True, "white")
    WIN.blit(window_text, (window_rect.centerx - window_text.get_width()//2,
                          window_rect.centery - window_text.get_height()//2))
    
    note = FONT_TINY.render("(Restart required for window size)", True, "gray")
    WIN.blit(note, (WIDTH//2 - note.get_width()//2, 360))
    
    #reset statistics button
    reset_rect = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)
    reset_color = (200, 80, 80) if reset_rect.collidepoint(mouse_pos) else (150, 50, 50)
    pygame.draw.rect(WIN, reset_color, reset_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", reset_rect, 3, border_radius=10)
    reset_text = FONT_TEXT.render("Reset Statistics", True, "white")
    WIN.blit(reset_text, (reset_rect.centerx - reset_text.get_width()//2,
                          reset_rect.centery - reset_text.get_height()//2))
    
    back_text = FONT_TINY.render("Press ESC to go back", True, "yellow")
    WIN.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 50))
    
    pygame.display.update()
    return window_rect, reset_rect

