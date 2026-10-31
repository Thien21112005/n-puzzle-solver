"""Turn a picture into puzzle plates."""

import pygame

from npuzzle.ui import draw, theme

REFERENCE_SIZE = 96


def center_square(picture: pygame.Surface) -> pygame.Surface:
    """Crop the largest centered square, so wide or tall pictures keep their proportions."""
    width, height = picture.get_size()
    side = min(width, height)
    return picture.subsurface(((width - side) // 2, (height - side) // 2, side, side))


class ImageTiles:
    """A loaded picture, cut into one plate per board cell."""

    def __init__(self, path: str, rows: int = 3, cols: int = 3):
        picture = center_square(pygame.image.load(path).convert_alpha())
        side = theme.PLATE
        pitch = side + theme.PLATE_GAP
        whole = pitch * cols - theme.PLATE_GAP
        scaled = pygame.transform.smoothscale(picture, (whole, whole))
        # Plates are prepared once, because rounding them on every frame is expensive.
        self.plates = []
        for row in range(rows):
            for col in range(cols):
                tile = pygame.Surface((side, side), pygame.SRCALPHA)
                tile.blit(scaled, (0, 0), (col * pitch, row * pitch, side, side))
                self.plates.append(draw.clip_rounded(tile, theme.PLATE_RADIUS))
        reference = pygame.transform.smoothscale(picture, (REFERENCE_SIZE, REFERENCE_SIZE))
        self.reference = draw.clip_rounded(reference, theme.CONTROL_RADIUS)

    def plate_for(self, value: int) -> pygame.Surface:
        """Return the plate of a value; 0 is the last cell, shown once the board is won."""
        return self.plates[value - 1]
