import pygame
import time
import math
import random
from logic import get_neighbors, get_connected_bubbles, pop_bubbles


    #Logica joc si cea care conteaza defapt phase 1

#Aici fac implementarea la generarea matricei
COLLUMS_NR = 8
ROWS_NR = 10

grid = []

for r in range(ROWS_NR):
    currect_row = []
    if r % 2 == 0:
        nr_bubbles_per_dis_row = COLLUMS_NR
    else:
        nr_bubbles_per_dis_row = COLLUMS_NR - 1
    
    for c in range(nr_bubbles_per_dis_row):
        currect_row.append(random.randint(1, 4))
    
    grid.append(currect_row)


#my_neighbors = get_neighbors(0, 1, ROWS_NR, COLLUMS_NR)
#print(f"Vecinii lui 0, 1 sunt {my_neighbors}")

i = 0
for row in grid:
    if i % 2 == 0:
        print(row)
    else:
        print(f"  {row}")
    i += 1

"""
grupul = get_connected_bubbles(grid, 5, 5)

print(f"Grupul pe care l am gasit care sa fie de tipul {grid[5][5]} este: {grupul}")

if pop_bubbles(grid, grupul) == True:
    print("Avem grup mai mare de 3. Afisam matricea")
    i = 0
    for row in grid:
        if i % 2 == 0:
            print(row)
        else:
            print(f"  {row}")
        i += 1
else:
    print("Nu avem grup mai mare de 3")
"""

        #Phase 2
WIDTH = 1000
HEIGHT = 800

MARGIN_WIDTH = 200
MARGIN_HEIGHT = 150

diam = (HEIGHT - MARGIN_HEIGHT) / ROWS_NR
radius = int(diam / 2)

start_x = (WIDTH - COLLUMS_NR * diam) / 2
start_y = (HEIGHT - ROWS_NR * diam) / 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")

#BG = pygame.transform.scale(pygame.image.load("bkgr.jpg"), (WIDTH, HEIGHT))
BG = pygame.image.load("bkgr.jpg")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

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


def main(grid):
    run = True
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
                        print("Group to small")

        draw_window(grid, hovered_bubble)
    
    pygame.quit()

if __name__ == "__main__":
    main(grid)