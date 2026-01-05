#This is the py file for settings regarding the game (like the dimensions of the window and tings in that regard)

import pygame
COLLUMS_NR = 8
ROWS_NR = 10

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