"""Colors, sizes and fonts of the interface."""

import pygame

GAME_WIDTH = 400
BOARD_HEIGHT = 400
PANEL_HEIGHT = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = BOARD_HEIGHT + PANEL_HEIGHT
TILE_SIZE = GAME_WIDTH // 3
TILE_GAP = 10
TILE_RADIUS = 10

BG_COLOR = (245, 245, 220)
EXTENDED_BG_COLOR = (220, 230, 240)
PANEL_COLOR = (230, 230, 230)
TILE_COLOR = (120, 160, 180)
EMPTY_COLOR = (220, 220, 220)
TEXT_COLOR = (50, 50, 50)
ACCENT_COLOR = (70, 130, 180)
BORDER_COLOR = (60, 60, 60)
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER = (80, 130, 180)
BUTTON_DISABLED = (180, 180, 180)
MENU_COLOR = (240, 240, 240)
MENU_HOVER = (200, 200, 200)
GREEN = (80, 200, 120)
GREEN_HOVER = (100, 220, 140)
TRASH_COLOR = (200, 80, 80)
TRASH_HOVER = (220, 100, 100)
RESET_COLOR = (150, 100, 200)
RESET_HOVER = (170, 120, 220)


class Fonts:
    def __init__(self):
        self.tile = pygame.font.SysFont("Arial", 50, bold=True)
        self.heading = pygame.font.SysFont("Arial", 20, bold=True)
        self.body = pygame.font.SysFont("Arial", 16, bold=True)
