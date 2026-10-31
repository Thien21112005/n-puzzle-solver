import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture
def display():
    pygame.init()
    yield pygame.display.set_mode((800, 600))
    pygame.quit()
