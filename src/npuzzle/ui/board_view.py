"""Draw the board and the reference picture."""

import pygame

from npuzzle.ui import theme
from npuzzle.ui.image_tiles import REFERENCE_SIZE, ImageTiles


def draw_background(screen: pygame.Surface) -> None:
    screen.fill(theme.BG_COLOR)
    side_area = pygame.Rect(
        theme.GAME_WIDTH, 0, theme.SCREEN_WIDTH - theme.GAME_WIDTH, theme.BOARD_HEIGHT
    )
    pygame.draw.rect(screen, theme.EXTENDED_BG_COLOR, side_area)
    pygame.draw.line(
        screen, theme.ACCENT_COLOR, (theme.GAME_WIDTH, 0), (theme.GAME_WIDTH, theme.BOARD_HEIGHT), 2
    )


def draw_board(
    screen: pygame.Surface, state, size: int, fonts: theme.Fonts, image: ImageTiles | None
) -> None:
    for index, value in enumerate(state):
        row, col = divmod(index, size)
        x = col * theme.TILE_SIZE + theme.TILE_GAP // 2
        y = row * theme.TILE_SIZE + theme.TILE_GAP // 2
        side = theme.TILE_SIZE - theme.TILE_GAP
        rect = pygame.Rect(x, y, side, side)

        if image:
            screen.blit(image.tile_for(value), rect)
        elif value:
            pygame.draw.rect(screen, theme.TILE_COLOR, rect, border_radius=theme.TILE_RADIUS)
            text = fonts.tile.render(str(value), True, theme.TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))
        else:
            pygame.draw.rect(screen, theme.EMPTY_COLOR, rect, border_radius=theme.TILE_RADIUS)


def draw_reference(screen: pygame.Surface, image: ImageTiles, fonts: theme.Fonts) -> None:
    x = theme.GAME_WIDTH + (theme.GAME_WIDTH - REFERENCE_SIZE) // 2
    y = (theme.BOARD_HEIGHT - REFERENCE_SIZE) // 2
    frame = pygame.Rect(x, y, REFERENCE_SIZE, REFERENCE_SIZE)
    pygame.draw.rect(screen, (255, 255, 255), frame, border_radius=15)
    pygame.draw.rect(screen, theme.ACCENT_COLOR, frame, 3, border_radius=15)
    screen.blit(image.reference, (x, y))
    label = fonts.body.render("Hình hoàn chỉnh", True, theme.TEXT_COLOR)
    screen.blit(label, (x + (REFERENCE_SIZE - label.get_width()) // 2, y + REFERENCE_SIZE + 10))
