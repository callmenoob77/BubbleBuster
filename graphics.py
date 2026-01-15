"""
Graphics module - handles all drawing and animations.

This includes bubbles, menus, overlays, pop/fall animations.
"""

import pygame
import math
from settings import *

# setup fonts
pygame.font.init()
FONT_TITLE = pygame.font.SysFont("Arial", 64)
FONT_BIG = pygame.font.SysFont("Arial", 48)
FONT_BUTTON = pygame.font.SysFont("Arial", 36)
FONT_TEXT = pygame.font.SysFont("Arial", 28)
FONT_SMALL = pygame.font.SysFont("Arial", 24)
FONT_TINY = pygame.font.SysFont("Arial", 20)

# dark overlays for menus
OVERLAY = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
OVERLAY.fill((0, 0, 0, 150))
OVERLAY_DARK = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
OVERLAY_DARK.fill((0, 0, 0, 180))


def get_pixel_coordinates(row, col, grid=None):
    """
    Convert grid position to screen pixel coords.
    
    Handles hexagonal offset for odd rows.
    
    Args:
        row: Grid row
        col: Grid column
        grid: Optional grid for dynamic sizing
        
    Returns:
        Tuple (x, y) pixel position for bubble center
    """
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
    
    # offset odd rows
    if row % 2 == 1:
        x += radius
        
    return int(x + radius), int(y + radius)


def get_mouse_coordinates(mouse_pos, grid):
    """
    Find which bubble mouse is hovering over.
    
    Args:
        mouse_pos: (x, y) mouse position
        grid: Game board
        
    Returns:
        (row, col) if over a bubble, None otherwise
    """
    mx, my = mouse_pos

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            bx, by = get_pixel_coordinates(r, c, grid)
            dist = math.sqrt((mx - bx)**2 + (my - by)**2)
            if dist < radius:
                return (r, c)
    
    return None


def draw_window(grid, hovered_bubble=None, bubbles_to_hide=[]):
    """
    Draw all bubbles on screen.
    
    Args:
        grid: Game board
        hovered_bubble: Optional (row,col) to highlight
        bubbles_to_hide: Positions to skip (for animations)
    """
    WIN.blit(BG, (0, 0))
    
    colors = ["white", "red", "blue", "green", "yellow", "purple", "cyan", "orange"]

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            val = grid[r][c]

            if (r, c) in bubbles_to_hide or val == 0:
                continue

            px, py = get_pixel_coordinates(r, c, grid)
            
            if val == 8:
                # stone - gray with border
                pygame.draw.circle(WIN, "gray", (px, py), radius - 2)
                pygame.draw.circle(WIN, "darkgray", (px, py), radius - 2, 3)
            elif 9 <= val <= 15:
                # bomb - colored with white center dot
                color = colors[val - 8]
                pygame.draw.circle(WIN, color, (px, py), radius - 2)
                pygame.draw.circle(WIN, "white", (px, py), radius // 3)
            else:
                # regular bubble
                pygame.draw.circle(WIN, colors[val], (px, py), radius - 2)

            # highlight if hovered
            if hovered_bubble == (r, c):
                pygame.draw.circle(WIN, "white", (px, py), radius, 3)


def pop_animation(grid, group, run_total, game_state=None):
    """
    Animate bubbles shrinking when popped.
    
    Args:
        grid: Game board
        group: List of positions being popped
        run_total: Score to show in UI
        game_state: For UI display
    """
    clock = pygame.time.Clock()
    colors = ["white", "red", "blue", "green", "yellow", "purple", "cyan", "orange"]

    frames = 10
    for i in range(frames, 0, -1):
        clock.tick(60)

        curr_rad = int(radius * (i / frames))
        draw_window(grid, bubbles_to_hide=group)

        if game_state:
            draw_ui(game_state, run_total)

        for r, c in group:
            val = grid[r][c]
            if val == 8:
                col = "gray"
            elif 9 <= val <= 15:
                col = colors[val - 8]
            else:
                col = colors[val]
            
            x, y = get_pixel_coordinates(r, c, grid)
            pygame.draw.circle(WIN, col, (x, y), curr_rad)
            if i > 7:
                pygame.draw.circle(WIN, col, (x, y), curr_rad, 2)
        
        pygame.display.update()


def falling_animation(grid, floating_bubbles, run_total, game_state=None):
    """
    Animate bubbles falling when detached.
    
    Args:
        grid: Game board
        floating_bubbles: Positions that are falling
        run_total: Score for UI
        game_state: For UI display
    """
    clock = pygame.time.Clock()
    colors = ["white", "red", "blue", "green", "yellow", "purple", "cyan", "orange"]
    
    # save starting positions
    bubble_info = []
    for r, c in floating_bubbles:
        x, y = get_pixel_coordinates(r, c, grid)
        val = grid[r][c]
        if val == 8:
            col = "gray"
        elif 9 <= val <= 15:
            col = colors[val - 8]
        else:
            col = colors[val]
        bubble_info.append((x, y, col))
    
    frames = 30
    for frame in range(frames):
        clock.tick(60)
        offset = int((frame / frames) * HEIGHT)
        
        draw_window(grid, bubbles_to_hide=floating_bubbles)
        
        if game_state:
            draw_ui(game_state, run_total)
        
        for x, y, col in bubble_info:
            pygame.draw.circle(WIN, col, (x, y + offset), radius - 2)
        
        pygame.display.update()


#=== UI Drawing ===#

def draw_ui(game_state, run_total):
    """
    Draw score, level, powers during gameplay.
    
    Args:
        game_state: Current game state
        run_total: Best score this run
    """
    # score
    txt = FONT_TEXT.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(txt, (20, 20))
    
    # best
    txt = FONT_TEXT.render(f"Best: {run_total}", True, "gold")
    WIN.blit(txt, (20, 55))
    
    # level
    txt = FONT_TEXT.render(f"Level: {game_state.level}", True, "white")
    WIN.blit(txt, (WIDTH - 130, 20))
    
    # hints
    txt = FONT_TINY.render("Press ENTER for next level  |  ESC for menu", True, "orange")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 40))
    
    # power indicator
    if game_state.color_powers > 0:
        txt = FONT_TEXT.render(f"COLOR x{game_state.color_powers} [C]", True, "cyan")
        WIN.blit(txt, (20, 90))
    
    # color mode message
    if game_state.color_mode and not game_state.selected_bubble:
        txt = FONT_TEXT.render("COLOR MODE - Click a bubble to change!", True, "yellow")
        WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 60))


def draw_color_picker(num_colors, selected_pos):
    """
    Draw color picker panel.
    
    Args:
        num_colors: How many colors to show
        selected_pos: Currently selected bubble position
        
    Returns:
        List of (rect, color_index) for click handling
    """
    colors = ["red", "blue", "green", "yellow", "purple", "cyan", "orange"]
    
    panel_w = 80
    panel_h = num_colors * 40 + 45
    panel_x = WIDTH - panel_w - 15
    panel_y = (HEIGHT - panel_h) // 2
    
    # draw panel background
    rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    pygame.draw.rect(WIN, (40, 40, 40), rect, border_radius=10)
    pygame.draw.rect(WIN, "cyan", rect, 3, border_radius=10)
    
    # title
    txt = FONT_TINY.render("PICK", True, "cyan")
    WIN.blit(txt, (panel_x + panel_w//2 - txt.get_width()//2, panel_y + 8))
    
    # color buttons
    buttons = []
    for i in range(num_colors):
        btn = pygame.Rect(panel_x + 15, panel_y + 35 + i * 40, 50, 30)
        pygame.draw.rect(WIN, colors[i], btn, border_radius=5)
        pygame.draw.rect(WIN, "white", btn, 2, border_radius=5)
        buttons.append((btn, i + 1))
    
    return buttons


def draw_level_complete(game_state):
    """
    Show level complete overlay.
    
    Args:
        game_state: For showing score
    """
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    txt = FONT_BIG.render("Level Complete!", True, "green")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 80))
    
    txt = FONT_TINY.render(f"Score: {game_state.score}", True, "white")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))
    
    if game_state.score >= game_state.high_score:
        txt = FONT_TINY.render("NEW HIGH SCORE!", True, "gold")
        WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 + 40))
    
    txt = FONT_TINY.render("Click to continue...", True, "yellow")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 + 90))
    
    pygame.display.update()


def draw_game_complete(run_total):
    """
    Show game finished screen.
    
    Args:
        run_total: Best score from the run
    """
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    txt = FONT_BIG.render("Good job!", True, "gold")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 120))
    
    txt = FONT_BIG.render("You finished the game!", True, "green")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
    
    txt = FONT_TEXT.render(f"Best Score: {run_total}", True, "gold")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 + 30))
    
    txt = FONT_TEXT.render("Press ESC to get to the menu", True, "yellow")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.update()


def draw_menu(mouse_pos):
    """
    Draw main menu.
    
    Args:
        mouse_pos: For button hover effects
        
    Returns:
        Tuple of button rects (start, stats, settings)
    """
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY, (0, 0))
    
    # title
    txt = FONT_TITLE.render("Bubble Buster", True, "white")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 150))
    
    # start button
    start_rect = pygame.Rect(WIDTH//2 - 120, 280, 240, 60)
    col = (100, 255, 100) if start_rect.collidepoint(mouse_pos) else (50, 200, 50)
    pygame.draw.rect(WIN, col, start_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", start_rect, 3, border_radius=10)
    txt = FONT_BUTTON.render("Start Game", True, "black")
    WIN.blit(txt, (start_rect.centerx - txt.get_width()//2, 
                   start_rect.centery - txt.get_height()//2))
    
    # stats button
    stats_rect = pygame.Rect(WIDTH//2 - 120, 360, 240, 60)
    col = (100, 100, 255) if stats_rect.collidepoint(mouse_pos) else (50, 50, 200)
    pygame.draw.rect(WIN, col, stats_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", stats_rect, 3, border_radius=10)
    txt = FONT_BUTTON.render("Statistics", True, "white")
    WIN.blit(txt, (stats_rect.centerx - txt.get_width()//2,
                   stats_rect.centery - txt.get_height()//2))
    
    # settings button
    settings_rect = pygame.Rect(WIDTH//2 - 120, 440, 240, 60)
    col = (180, 100, 200) if settings_rect.collidepoint(mouse_pos) else (128, 50, 150)
    pygame.draw.rect(WIN, col, settings_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", settings_rect, 3, border_radius=10)
    txt = FONT_BUTTON.render("Settings", True, "white")
    WIN.blit(txt, (settings_rect.centerx - txt.get_width()//2,
                   settings_rect.centery - txt.get_height()//2))
    
    # hints
    txt = FONT_TINY.render("Press ENTER to skip to the next level", True, "white")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 550))
    
    txt = FONT_TINY.render("Press ESC to return to menu", True, "gray")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 580))
    
    pygame.display.update()
    return start_rect, stats_rect, settings_rect


def draw_stats(stats):
    """
    Draw statistics screen.
    
    Args:
        stats: Dict with all stat values
    """
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    txt = FONT_BIG.render("Statistics", True, "cyan")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 80))
    
    y = 160
    lines = [
        f"High Score: {stats['high_score']}",
        f"Total Bubbles Popped: {stats['total_bubbles']}",
        f"Games Played: {stats['games_played']}",
        f"Levels Completed: {stats['levels_completed']}"
    ]
    
    for line in lines:
        txt = FONT_TEXT.render(line, True, "white")
        WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
        y += 45
    
    # level scores section
    y += 20
    txt = FONT_TEXT.render("Level High Scores:", True, "gold")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
    y += 40
    
    level_scores = stats.get("level_scores", {})
    if level_scores:
        cols = 4
        col_w = 200
        sx = WIDTH//2 - (cols * col_w)//2
        for i, (lvl, score) in enumerate(sorted(level_scores.items(), key=lambda x: int(x[0]))):
            col = i % cols
            row = i // cols
            x = sx + col * col_w
            ly = y + row * 30
            txt = FONT_TINY.render(f"Level {lvl}: {score}", True, "white")
            WIN.blit(txt, (x, ly))
    
    txt = FONT_TINY.render("Press ESC to go back", True, "yellow")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 50))
    
    pygame.display.update()


def draw_settings(settings, mouse_pos):
    """
    Draw settings screen.
    
    Args:
        settings: Current settings dict
        mouse_pos: For hover effects
        
    Returns:
        Tuple of button rects (window, reset)
    """
    WIN.blit(BG, (0, 0))
    WIN.blit(OVERLAY_DARK, (0, 0))
    
    txt = FONT_BIG.render("Settings", True, "purple")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 150))
    
    # window size toggle
    window_rect = pygame.Rect(WIDTH//2 - 150, 280, 300, 60)
    col = "green" if settings.get("large_window", False) else "red"
    pygame.draw.rect(WIN, col, window_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", window_rect, 3, border_radius=10)
    status = "ON" if settings.get("large_window", False) else "OFF"
    txt = FONT_TEXT.render(f"Large Window: {status}", True, "white")
    WIN.blit(txt, (window_rect.centerx - txt.get_width()//2,
                   window_rect.centery - txt.get_height()//2))
    
    txt = FONT_TINY.render("(Restart required for window size)", True, "gray")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 360))
    
    # reset stats button
    reset_rect = pygame.Rect(WIDTH//2 - 150, 400, 300, 60)
    col = (200, 80, 80) if reset_rect.collidepoint(mouse_pos) else (150, 50, 50)
    pygame.draw.rect(WIN, col, reset_rect, border_radius=10)
    pygame.draw.rect(WIN, "white", reset_rect, 3, border_radius=10)
    txt = FONT_TEXT.render("Reset Statistics", True, "white")
    WIN.blit(txt, (reset_rect.centerx - txt.get_width()//2,
                   reset_rect.centery - txt.get_height()//2))
    
    txt = FONT_TINY.render("Press ESC to go back", True, "yellow")
    WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 50))
    
    pygame.display.update()
    return window_rect, reset_rect
