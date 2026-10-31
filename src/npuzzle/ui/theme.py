"""Design tokens: Hanoi limewash walls and enamel house-number plates."""

import pygame

from npuzzle.paths import asset_path

WINDOW_SIZE = (1100, 680)
UNIT = 8

WALL = (227, 168, 43)
WALL_SHADE = (196, 142, 28)
WALL_DEEP = (166, 118, 20)
COBALT = (18, 60, 156)
COBALT_DEEP = (12, 44, 118)
ENAMEL = (246, 245, 238)
ENAMEL_SHADE = (232, 230, 220)
SHUTTER = (47, 107, 79)
SHUTTER_DEEP = (36, 84, 62)
INK = (26, 26, 26)
INK_SOFT = (72, 72, 76)
ERROR = (160, 44, 24)
RULE = (196, 201, 214)
SELECTED = (222, 229, 245)
HOVER = (236, 236, 232)
DISABLED_FILL = (222, 220, 210)
DISABLED_TEXT = (92, 90, 84)

MARGIN = 4 * UNIT
PLATE = 136
PLATE_GAP = 12
PLATE_RADIUS = 14
PLATE_RIM = 6
PANEL_RADIUS = 14
CONTROL_RADIUS = 8
CONTROL_HEIGHT = 44

HOVER_LIFT = 3
SLIDE_MS = 130
RIPPLE_STEP_MS = 70
RIPPLE_FADE_MS = 220


def _font(weight: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(asset_path("fonts", f"BeVietnamPro-{weight}.ttf"), size)


class Fonts:
    def __init__(self):
        self.plate = _font("Bold", 72)
        self.title = _font("ExtraBold", 44)
        self.count = _font("Bold", 30)
        self.heading = _font("Bold", 20)
        self.strong = _font("Bold", 15)
        self.data = _font("Regular", 17)
        self.data_best = _font("Bold", 17)
        self.small = _font("Regular", 14)
        self.small_bold = _font("Bold", 13)
