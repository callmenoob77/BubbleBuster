#This is the py file for the graphics part, like the popping of the baloons and tings like that

import pygame
import math
from settings import *

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


def get_mouse_coordinates(mouse_pos, grid):
    mx, my = mouse_pos

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            bubble_x, bubble_y = get_pixel_coordinates(r, c, grid)
            distanta = math.sqrt((mx - bubble_x)**2 + (my - bubble_y)**2)

            if distanta < radius:
                return (r, c)
    return None


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

            color = colors[value]
            pos_row, pos_col = get_pixel_coordinates(r, c, grid)

            pygame.draw.circle(WIN, color, (pos_row, pos_col), radius - 2)

            if hovered_bubble == (r, c):
                pygame.draw.circle(WIN, "white", (pos_row, pos_col), radius, 3)


def pop_animation(grid, group, game_state=None):
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
            draw_ui(game_state)

        for r, c in group:
            value = grid[r][c]
            color = colors[value]
            x, y = get_pixel_coordinates(r, c, grid)

            pygame.draw.circle(WIN, color, (x, y), current_radius)
            if i > 7:
                pygame.draw.circle(WIN, color, (x, y), current_radius, 2)
        pygame.display.update()


def falling_animation(grid, floating_bubbles, game_state=None):
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
        color = colors[grid[r][c]]
        bubbles_data.append((x, y, color))
    
    frames = 30
    fall_distance = HEIGHT
    
    for frame in range(frames):
        clock.tick(60)
        offset = int((frame / frames) * fall_distance)
        
        draw_window(grid, hovered_bubble=None, bubbles_to_hide=floating_bubbles)
        
        if game_state:
            draw_ui(game_state)
        
        for x, y, color in bubbles_data:
            new_y = y + offset
            pygame.draw.circle(WIN, color, (x, new_y), radius - 2)
        
        pygame.display.update()


#Phase 4

def draw_ui(game_state):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 28)
    font_small = pygame.font.SysFont("Arial", 20)
    
    score_text = font.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(score_text, (20, 20))
    
    high_score_text = font.render(f"Best: {game_state.high_score}", True, "gold")
    WIN.blit(high_score_text, (20, 55))
    
    level_text = font.render(f"Level: {game_state.level}", True, "white")
    WIN.blit(level_text, (WIDTH - 130, 20))
    
    hint_text = font_small.render("Press ENTER for next level  |  ESC for menu", True, "orange")
    WIN.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 40))


def draw_level_complete(game_state):
    pygame.font.init()
    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 28)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    WIN.blit(overlay, (0, 0))
    
    text = font_big.render("Level Complete!", True, "green")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
    
    score = font_small.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2))
    
    if game_state.score >= game_state.high_score:
        new_high = font_small.render("NEW HIGH SCORE!", True, "gold")
        WIN.blit(new_high, (WIDTH//2 - new_high.get_width()//2, HEIGHT//2 + 40))
    
    prompt = font_small.render("Click to continue...", True, "yellow")
    WIN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 90))
    
    pygame.display.update()


def draw_game_complete(game_state):
    pygame.font.init()
    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 28)
    
    WIN.blit(BG, (0, 0))
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    WIN.blit(overlay, (0, 0))
    
    text = font_big.render("Good job!", True, "gold")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 120))
    
    text2 = font_big.render("You finished the game!", True, "green")
    WIN.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 50))
    
    high = font_small.render(f"High Score: {game_state.high_score}", True, "gold")
    WIN.blit(high, (WIDTH//2 - high.get_width()//2, HEIGHT//2 + 30))
    
    prompt = font_small.render("Press ESC to get to the menu", True, "yellow")
    WIN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.update()

def draw_menu(high_score):
    pygame.font.init()
    font_title = pygame.font.SysFont("Arial", 64)
    font_button = pygame.font.SysFont("Arial", 36)
    font_small = pygame.font.SysFont("Arial", 24)
    
    WIN.blit(BG, (0, 0))
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    WIN.blit(overlay, (0, 0))
    
    title = font_title.render("Bubble Buster", True, "white")
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    
    high_text = font_small.render(f"High Score: {high_score}", True, "gold")
    WIN.blit(high_text, (WIDTH//2 - high_text.get_width()//2, 230))
    
    button_rect = pygame.Rect(WIDTH//2 - 120, 350, 240, 70)
    pygame.draw.rect(WIN, "green", button_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", button_rect, 3, border_radius=10)
    
    btn_text = font_button.render("Start Game", True, "black")
    WIN.blit(btn_text, (button_rect.centerx - btn_text.get_width()//2, 
                       button_rect.centery - btn_text.get_height()//2))
    
    instructions = font_small.render("Press ENTER during game to skip to next level", True, "white")
    WIN.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 500))
    
    esc_text = font_small.render("Press ESC to return to menu", True, "gray")
    WIN.blit(esc_text, (WIDTH//2 - esc_text.get_width()//2, 540))
    
    pygame.display.update()
    return button_rect
