#This is the py file for the graphics part, like the popping of the baloons and tings like that

import pygame
import math
from settings import *

def get_pixel_coordinates(row, col):
    x = start_x + (col * diam)
    y = start_y + (row * diam)
    
    # Zig Zag shift
    if row % 2 == 1:
        x += radius
        
    # Return center (x + radius, y + radius)
    return int(x + radius), int(y + radius)


def get_mouse_coordinates(mouse_pos, grid):
    mx, my = mouse_pos

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            bubble_x, bubble_y = get_pixel_coordinates(r, c)
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
        "orange"
    ]

    for r in range(ROWS_NR):
        for c in range(len(grid[r])):
            value = grid[r][c]

            if (r, c) in bubbles_to_hide:
                continue

            color = colors[value]
            pos_row, pos_col = get_pixel_coordinates(r, c)

            pygame.draw.circle(WIN, color, (pos_row, pos_col), radius - 2)

            if hovered_bubble == (r, c):
                pygame.draw.circle(WIN, "white", (pos_row, pos_col), radius, 3)

    pygame.display.update()


def pop_animation(grid, group):
    clock = pygame.time.Clock()
    colors = [
        "white",
        "red",
        "blue",
        "green",
        "yellow",
        "orange"
    ]

    frames = 10

    for i in range(frames, 0, -1):
        clock.tick(60)

        current_radius = int(radius * (i / frames))

        draw_window(grid, hovered_bubble = None, bubbles_to_hide = group)

        for r, c in group:
            value = grid[r][c]
            color = colors[value]
            x, y = get_pixel_coordinates(r, c)

            pygame.draw.circle(WIN, color, (x, y), current_radius)
            if i > 7:
                pygame.draw.circle(WIN, color, (x, y), current_radius, 2)
        pygame.display.update()