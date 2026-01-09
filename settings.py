#This is the py file for settings regarding the game

import pygame
import json
import os

#load saved settings for window size
def get_large_window_setting():
    if os.path.exists("save_data.json"):
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
                return data.get("settings", {}).get("large_window", False)
        except:
            return False
    return False

#window settings - larger if setting is on
if get_large_window_setting():
    WIDTH = 1200
    HEIGHT = 900
else:
    WIDTH = 1000
    HEIGHT = 800

#bubble size (used for drawing and hit detection)
MAX_ROWS = 12
MAX_COLS = 10
diam = (HEIGHT - 100) / MAX_ROWS
radius = int(diam / 2)

#starting position (used as fallback)
start_x = (WIDTH - MAX_COLS * diam) / 2
start_y = (HEIGHT - MAX_ROWS * diam) / 2

#game window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")
BG = pygame.image.load("bkgr.jpg")

#level settings (used in logic.py)
MAX_LEVEL = 20
BASE_ROWS = 5
BASE_COLS = 6
MAX_COLORS = 7