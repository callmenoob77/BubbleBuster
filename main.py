import pygame
import time
import math
import random
from logic import *
from settings import *
from graphics import *

grid = []


def generate_grid():
    for r in range(ROWS_NR):
        currect_row = []
        if r % 2 == 0:
            nr_bubbles_per_dis_row = COLLUMS_NR
        else:
            nr_bubbles_per_dis_row = COLLUMS_NR - 1
        
        for c in range(nr_bubbles_per_dis_row):
            currect_row.append(random.randint(1, 4))
        
        grid.append(currect_row)


def main(grid):
    run = True
    generate_grid()
    clock = pygame.time.Clock()

    pygame.display.update()

    while run:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()
        hovered_bubble = get_mouse_coordinates(mouse_pos, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #for da baloon popping
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hovered_bubble is not None:
                    row, col = hovered_bubble

                    group = get_connected_bubbles(grid, row, col)
                    if len(group) >= 3:
                        pop_animation(grid, group)

                        pop_bubbles(grid, group)
                        print(f"I popped {len(group)} bubbles")
                    else:
                        print("Group too small")

        draw_window(grid, hovered_bubble)
    
    pygame.quit()

if __name__ == "__main__":
    main(grid)