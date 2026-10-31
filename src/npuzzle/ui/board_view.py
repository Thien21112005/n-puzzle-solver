"""The board: enamel plates on the wall, with the slide and the win ripple."""

import pygame

from npuzzle.core.board import BLANK, State
from npuzzle.ui import draw, theme
from npuzzle.ui.image_tiles import ImageTiles

SCREW_RADIUS = 3
SCREW_INSET = 16


def _plate_surface(fill, fonts: theme.Fonts, value: int) -> pygame.Surface:
    side = theme.PLATE
    plate = draw.rounded(
        (side, side), theme.PLATE_RADIUS, fill, theme.ENAMEL, theme.PLATE_RIM
    ).copy()
    for y in (SCREW_INSET, side - SCREW_INSET - 1):
        pygame.draw.circle(plate, theme.ENAMEL, (side // 2, y), SCREW_RADIUS)
    numeral = fonts.plate.render(str(value), True, theme.ENAMEL)
    plate.blit(numeral, numeral.get_rect(center=(side // 2, side // 2 - 2)))
    return plate


class BoardView:
    def __init__(self, origin: tuple[int, int], fonts: theme.Fonts, size: int = 3):
        self.origin = origin
        self.fonts = fonts
        self.size = size
        self._state: State | None = None
        self._slide: tuple[int, int, int, int] | None = None  # value, from index, to index, start
        self._won_at: int | None = None
        self._plates: dict[tuple[int, int, int, int], pygame.Surface] = {}
        pitch = theme.PLATE + theme.PLATE_GAP
        whole = pitch * size - theme.PLATE_GAP
        self.rect = pygame.Rect(origin, (whole, whole))

    def cell_position(self, index: int) -> tuple[int, int]:
        row, col = divmod(index, self.size)
        pitch = theme.PLATE + theme.PLATE_GAP
        return self.origin[0] + col * pitch, self.origin[1] + row * pitch

    def cell_at(self, pos) -> int | None:
        """Return the index of the cell under a point, if any."""
        for index in range(self.size * self.size):
            x, y = self.cell_position(index)
            if pygame.Rect(x, y, theme.PLATE, theme.PLATE).collidepoint(pos):
                return index
        return None

    def sync(self, state: State, won: bool, now_ms: int) -> None:
        """Start the animations that a change of state calls for."""
        if self._state is not None and state != self._state:
            changed = [i for i in range(len(state)) if state[i] != self._state[i]]
            if len(changed) == 2:
                target = next(i for i in changed if state[i] != BLANK)
                origin = next(i for i in changed if i != target)
                self._slide = (state[target], origin, target, now_ms)
            else:
                self._slide = None
        self._state = state
        if won and self._won_at is None:
            self._won_at = now_ms
        elif not won:
            self._won_at = None

    def _plate_position(self, index: int, value: int, now_ms: int) -> tuple[float, float]:
        if self._slide and self._slide[0] == value:
            _, origin, target, started = self._slide
            amount = (now_ms - started) / theme.SLIDE_MS
            if amount < 1:
                ox, oy = self.cell_position(origin)
                tx, ty = self.cell_position(target)
                eased = draw.ease_out(amount)
                return ox + (tx - ox) * eased, oy + (ty - oy) * eased
        return self.cell_position(index)

    def _ripple(self, index: int, now_ms: int) -> float:
        """Return how far a plate has turned green, in reading order after a win."""
        if self._won_at is None:
            return 0.0
        elapsed = now_ms - self._won_at - index * theme.RIPPLE_STEP_MS
        return max(0.0, min(1.0, elapsed / theme.RIPPLE_FADE_MS))

    def _numbered_plate(self, value: int, ripple: float) -> pygame.Surface:
        fill = draw.lerp_color(theme.COBALT, theme.SHUTTER, ripple)
        key = (value, *fill)
        if key not in self._plates:
            self._plates[key] = _plate_surface(fill, self.fonts, value)
        return self._plates[key]

    def draw(self, screen, state: State, image: ImageTiles | None, now_ms: int) -> None:
        recess = draw.rounded((theme.PLATE, theme.PLATE), theme.PLATE_RADIUS, theme.WALL_SHADE)
        for index in range(len(state)):
            screen.blit(recess, self.cell_position(index))

        shadow = draw.soft_shadow((theme.PLATE, theme.PLATE), theme.PLATE_RADIUS, 110)
        for index, value in enumerate(state):
            # A won picture fills its gap, so the player sees the finished image.
            if value == BLANK and not (self._won_at is not None and image):
                continue
            x, y = self._plate_position(index, value, now_ms)
            screen.blit(shadow, (x - 8, y - 5))
            if image:
                plate = image.plate_for(value or len(state))
            else:
                plate = self._numbered_plate(value, self._ripple(index, now_ms))
            screen.blit(plate, (x, y))
