"""Drawing helpers that pygame lacks: smooth corners, soft shadows and aligned digits."""

import random
from functools import lru_cache

import pygame

SUPERSAMPLE = 4


@lru_cache(maxsize=256)
def rounded(
    size: tuple[int, int],
    radius: int,
    fill: tuple[int, int, int],
    border: tuple[int, int, int] | None = None,
    border_width: int = 0,
) -> pygame.Surface:
    """Return an antialiased rounded rectangle; pygame's own corners are jagged."""
    width, height = size
    large = pygame.Surface((width * SUPERSAMPLE, height * SUPERSAMPLE), pygame.SRCALPHA)
    # Transparent pixels share the edge color, or scaling down leaves a dark fringe.
    large.fill((*(border if border is not None else fill)[:3], 0))
    outer = large.get_rect()
    if border is not None:
        pygame.draw.rect(large, border, outer, border_radius=radius * SUPERSAMPLE)
        inset = border_width * SUPERSAMPLE
        inner_radius = max(radius - border_width, 0) * SUPERSAMPLE
        pygame.draw.rect(
            large, fill, outer.inflate(-2 * inset, -2 * inset), border_radius=inner_radius
        )
    else:
        pygame.draw.rect(large, fill, outer, border_radius=radius * SUPERSAMPLE)
    return pygame.transform.smoothscale(large, size)


@lru_cache(maxsize=32)
def soft_shadow(size: tuple[int, int], radius: int, alpha: int, spread: int = 8) -> pygame.Surface:
    """Return a blurred shadow, larger than `size` by `spread` on every side."""
    width, height = size
    canvas = pygame.Surface((width + 2 * spread, height + 2 * spread), pygame.SRCALPHA)
    shape = rounded(size, radius, (70, 45, 5))
    shape = shape.copy()
    shape.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
    canvas.blit(shape, (spread, spread))
    small = pygame.transform.smoothscale(
        canvas, (canvas.get_width() // 6, canvas.get_height() // 6)
    )
    return pygame.transform.smoothscale(small, canvas.get_size())


def dot(screen, center: tuple[int, int], radius: int, color) -> None:
    """Draw an antialiased circle."""
    surface = rounded((radius * 2, radius * 2), radius, color)
    screen.blit(surface, surface.get_rect(center=center))


def focus_ring(screen, rect: pygame.Rect, radius: int, color) -> None:
    """Outline a focused control with a clear gap around it."""
    outer = rect.inflate(6, 6)
    ring = rounded(outer.size, radius + 3, (*color, 0), color, 2)
    screen.blit(ring, outer)


def _brush_mark(strength: int) -> pygame.Surface:
    """Return one soft, round mark that fades to nothing at its edge."""
    side = 64
    mark = pygame.Surface((side, side))
    for radius in range(side // 2, 0, -1):
        amount = 1 - radius / (side / 2)
        shade = round(strength * amount * amount * (3 - 2 * amount))
        pygame.draw.circle(mark, (shade, shade, shade), (side // 2, side // 2), radius)
    return mark


@lru_cache(maxsize=4)
def limewash(size: tuple[int, int], color: tuple[int, int, int]) -> pygame.Surface:
    """Paint a wall with the wide, uneven brush marks of limewash."""
    rng = random.Random(7)
    wall = pygame.Surface(size)
    wall.fill(color)
    marks = {strength: _brush_mark(strength) for strength in (3, 5, 7)}
    for _ in range(160):
        mark = marks[rng.choice((3, 5, 7))]
        width = rng.randint(160, 520)
        height = rng.randint(70, 240)
        stroke = pygame.transform.smoothscale(mark, (width, height))
        position = (rng.randint(-width // 2, size[0]), rng.randint(-height // 2, size[1]))
        flag = pygame.BLEND_RGB_ADD if rng.random() < 0.5 else pygame.BLEND_RGB_SUB
        wall.blit(stroke, position, None, flag)
    return wall


def clip_rounded(surface: pygame.Surface, radius: int) -> pygame.Surface:
    """Cut a surface to rounded corners."""
    result = surface.copy().convert_alpha()
    mask = rounded(surface.get_size(), radius, (255, 255, 255))
    result.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    return result


def lerp_color(start, end, amount: float) -> tuple[int, int, int]:
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end, strict=True))


def ease_out(amount: float) -> float:
    """Exponential ease-out over the range 0 to 1."""
    return 1.0 if amount >= 1 else 1 - 2 ** (-10 * amount)


@lru_cache(maxsize=1024)
def _render(font: pygame.font.Font, text: str, color: tuple[int, int, int]) -> pygame.Surface:
    return font.render(text, True, color)


def text(screen, font, content: str, color, **anchor) -> pygame.Rect:
    """Draw text placed by a Rect attribute, for example midleft=(10, 20)."""
    surface = _render(font, content, color)
    rect = surface.get_rect(**anchor)
    screen.blit(surface, rect)
    return rect


def tabular_width(font, content: str) -> int:
    digit = font.size("0")[0]
    return sum(digit if char.isdigit() else font.size(char)[0] for char in content)


def tabular_text(screen, font, content: str, color, right: int, centery: int) -> None:
    """Draw right-aligned text with equal-width digits, so columns of numbers line up.

    The bundled font has proportional digits and pygame cannot enable tabular figures.
    """
    digit = font.size("0")[0]
    x = right - tabular_width(font, content)
    for char in content:
        surface = _render(font, char, color)
        width = digit if char.isdigit() else surface.get_width()
        screen.blit(
            surface, surface.get_rect(midtop=(x + width // 2, centery - surface.get_height() // 2))
        )
        x += width


def fit_text(font, content: str, width: int) -> str:
    """Shorten text with an ellipsis when it would overflow."""
    if font.size(content)[0] <= width:
        return content
    while content and font.size(content + "…")[0] > width:
        content = content[:-1]
    return content.rstrip() + "…"
