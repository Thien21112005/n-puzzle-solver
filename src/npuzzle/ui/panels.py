"""The control panel below the board: status text, buttons and algorithm menu."""

import pygame

from npuzzle.core.session import GameSession
from npuzzle.core.solvers import ALGORITHMS
from npuzzle.paths import asset_path
from npuzzle.ui import theme

BUTTON_WIDTH = 80
BUTTON_HEIGHT = 35
BUTTON_MARGIN = 10
ICON_BUTTON_SIZE = 35
ICON_SIZE = 20


def _load_icon(name: str) -> pygame.Surface:
    icon = pygame.image.load(asset_path("icons", name)).convert_alpha()
    return pygame.transform.smoothscale(icon, (ICON_SIZE, ICON_SIZE))


class ControlPanel:
    def __init__(self, fonts: theme.Fonts):
        self.fonts = fonts
        self.menu_open = False
        self.trash_icon = _load_icon("trash.png")
        self.reset_icon = _load_icon("reset.png")

        y = theme.BOARD_HEIGHT + 80
        names = ["shuffle", "choose", "algorithm", "solve"]
        total = len(names) * BUTTON_WIDTH + (len(names) - 1) * BUTTON_MARGIN
        x = (theme.SCREEN_WIDTH - total) // 2
        self.buttons = {
            name: pygame.Rect(
                x + index * (BUTTON_WIDTH + BUTTON_MARGIN), y, BUTTON_WIDTH, BUTTON_HEIGHT
            )
            for index, name in enumerate(names)
        }
        top = theme.BOARD_HEIGHT + 10
        reset_x = theme.SCREEN_WIDTH - ICON_BUTTON_SIZE - 10
        self.reset_rect = pygame.Rect(reset_x, top, ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)
        trash_x = reset_x - ICON_BUTTON_SIZE - 5
        self.trash_rect = pygame.Rect(trash_x, top, ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)

        algorithm = self.buttons["algorithm"]
        menu_top = y - BUTTON_HEIGHT * len(ALGORITHMS)
        self.menu_options = {
            name: pygame.Rect(
                algorithm.x, menu_top + index * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
            )
            for index, name in enumerate(ALGORITHMS)
        }

    def _draw_frame(self, screen, rect, base, hover, enabled=True, disabled=None):
        over = rect.collidepoint(pygame.mouse.get_pos())
        color = disabled if not enabled and disabled else hover if over else base
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, theme.BORDER_COLOR, rect, 2, border_radius=8)

    def _draw_button(self, screen, rect, label, base, hover, enabled=True, disabled=None):
        self._draw_frame(screen, rect, base, hover, enabled, disabled)
        text = self.fonts.body.render(label, True, theme.TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))

    def _draw_icon_button(self, screen, rect, icon, base, hover):
        self._draw_frame(screen, rect, base, hover)
        screen.blit(icon, icon.get_rect(center=rect.center))

    def _draw_centered(self, screen, font, text, color, y):
        surface = font.render(text, True, color)
        screen.blit(surface, (theme.SCREEN_WIDTH // 2 - surface.get_width() // 2, y))

    def draw(self, screen, session: GameSession, using_image: bool) -> None:
        panel = pygame.Rect(0, theme.BOARD_HEIGHT, theme.SCREEN_WIDTH, theme.PANEL_HEIGHT)
        pygame.draw.rect(screen, theme.PANEL_COLOR, panel)
        pygame.draw.line(
            screen,
            theme.ACCENT_COLOR,
            (0, theme.BOARD_HEIGHT),
            (theme.SCREEN_WIDTH, theme.BOARD_HEIGHT),
            2,
        )
        top = theme.BOARD_HEIGHT
        self._draw_centered(
            screen, self.fonts.heading, f"Moves: {session.moves}", theme.TEXT_COLOR, top + 15
        )
        if session.solving:
            if session.searching:
                status = f"Đang tìm giải pháp bằng {session.algorithm}..."
            else:
                status = f"Đang giải bằng {session.algorithm}: {len(session.solution)} bước còn lại"
            self._draw_centered(screen, self.fonts.body, status, theme.ACCENT_COLOR, top + 45)
        elif session.no_solution:
            status = f"Không tìm thấy giải pháp bằng {session.algorithm}"
            self._draw_centered(screen, self.fonts.body, status, theme.ACCENT_COLOR, top + 45)

        self._draw_button(
            screen, self.buttons["shuffle"], "Shuffle", theme.GREEN, theme.GREEN_HOVER
        )
        self._draw_button(
            screen, self.buttons["choose"], "Choose", theme.BUTTON_COLOR, theme.BUTTON_HOVER
        )
        self._draw_button(
            screen,
            self.buttons["algorithm"],
            session.algorithm,
            theme.BUTTON_COLOR,
            theme.BUTTON_HOVER,
        )
        self._draw_button(
            screen,
            self.buttons["solve"],
            "Cancel" if session.solving else "Solve",
            theme.BUTTON_COLOR,
            theme.BUTTON_HOVER,
            enabled=not session.won,
            disabled=theme.BUTTON_DISABLED,
        )
        if self.menu_open:
            for name, rect in self.menu_options.items():
                self._draw_button(screen, rect, name, theme.MENU_COLOR, theme.MENU_HOVER)

        self._draw_icon_button(
            screen, self.reset_rect, self.reset_icon, theme.RESET_COLOR, theme.RESET_HOVER
        )
        if using_image:
            self._draw_icon_button(
                screen, self.trash_rect, self.trash_icon, theme.TRASH_COLOR, theme.TRASH_HOVER
            )
        if session.won:
            self._draw_centered(screen, self.fonts.heading, "YOU WIN!", theme.GREEN, top + 120)
