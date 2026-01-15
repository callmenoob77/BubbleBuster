"""
Settings module - game config and pygame setup.

Window size is loaded from save file before pygame starts.
"""

import pygame
import json
import os


def get_large_window_setting():
    """
    Check if large window mode is enabled.
    
    Returns:
        True for large window, False for normal
    """
    if os.path.exists("save_data.json"):
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
                return data.get("settings", {}).get("large_window", False)
        except:
            return False
    return False


# set window size based on saved preference
if get_large_window_setting():
    WIDTH = 1200
    HEIGHT = 900
else:
    WIDTH = 1000
    HEIGHT = 800

# grid dimensions
MAX_ROWS = 12
MAX_COLS = 10

# calculate bubble size to fit grid
diam = (HEIGHT - 100) / MAX_ROWS
radius = int(diam / 2)

# default grid position (fallback)
start_x = (WIDTH - MAX_COLS * diam) / 2
start_y = (HEIGHT - MAX_ROWS * diam) / 2

# pygame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Buster")
BG = pygame.image.load("bkgr.jpg")

# level config
MAX_LEVEL = 20
BASE_ROWS = 5
BASE_COLS = 6
MAX_COLORS = 7