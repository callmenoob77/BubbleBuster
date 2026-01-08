#This is the py file for settings regarding the game (like the dimensions of the window and tings in that regard)

import pygame
COLLUMS_NR = 10
ROWS_NR = 12

WIDTH = 1000
HEIGHT = 800

MARGIN_WIDTH = 100
MARGIN_HEIGHT = 100

diam = (HEIGHT - MARGIN_HEIGHT) / ROWS_NR
radius = int(diam / 2)

start_x = (WIDTH - COLLUMS_NR * diam) / 2
start_y = (HEIGHT - ROWS_NR * diam) / 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")

#BG = pygame.transform.scale(pygame.image.load("bkgr.jpg"), (WIDTH, HEIGHT))
BG = pygame.image.load("bkgr.jpg")