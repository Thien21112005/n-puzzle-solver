"""Turn a picture into puzzle tiles."""

import pygame

from npuzzle.ui.theme import BOARD_HEIGHT, GAME_WIDTH, TILE_GAP, TILE_RADIUS, TILE_SIZE

REFERENCE_SIZE = 150


def rounded(surface: pygame.Surface, radius: int) -> pygame.Surface:
    width, height = surface.get_size()
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius)
    result = surface.copy().convert_alpha()
    result.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    return result


def center_square(picture: pygame.Surface) -> pygame.Surface:
    """Crop the largest centered square, so wide or tall pictures keep their proportions."""
    width, height = picture.get_size()
    side = min(width, height)
    return picture.subsurface(((width - side) // 2, (height - side) // 2, side, side))


class ImageTiles:
    """A loaded picture, cut into one tile per board cell."""

    def __init__(self, path: str, rows: int = 3, cols: int = 3):
        picture = center_square(pygame.image.load(path).convert_alpha())
        scaled = pygame.transform.smoothscale(
            picture, (GAME_WIDTH - TILE_GAP, BOARD_HEIGHT - TILE_GAP)
        )
        side = TILE_SIZE - TILE_GAP
        self.tiles = []
        for row in range(rows):
            for col in range(cols):
                tile = pygame.Surface((side, side), pygame.SRCALPHA)
                tile.blit(scaled, (0, 0), (col * TILE_SIZE, row * TILE_SIZE, side, side))
                self.tiles.append(tile)
        self.reference = pygame.transform.smoothscale(scaled, (REFERENCE_SIZE, REFERENCE_SIZE))
        # Rounding every tile on every frame is expensive, so it happens once here.
        self._rendered = [rounded(tile, TILE_RADIUS) for tile in self.tiles]
        faded = pygame.transform.grayscale(self.tiles[-1])
        faded.set_alpha(128)
        self._blank = rounded(faded, TILE_RADIUS)

    def tile_for(self, value: int) -> pygame.Surface:
        """Return the tile of a value; the blank shows the last cell, faded."""
        return self._rendered[value - 1] if value else self._blank
