"""Game loop and event handling."""

from tkinter import Tk, filedialog

import pygame

from npuzzle.core.board import BLANK, neighbors
from npuzzle.core.session import GameSession
from npuzzle.i18n import Translator, format_count
from npuzzle.settings import Settings
from npuzzle.ui import draw, theme
from npuzzle.ui.board_view import BoardView
from npuzzle.ui.image_tiles import ImageTiles
from npuzzle.ui.panels import SidePanel

ARROW_MOVES = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}
LEFT_COLUMN = theme.MARGIN
BOARD_TOP = 92
PANEL_LEFT = 496


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(theme.WINDOW_SIZE)
        self.settings = Settings.load()
        self.t = Translator(self.settings.language)
        self.clock = pygame.time.Clock()
        self.fonts = theme.Fonts()
        self.session = GameSession()
        self.board = BoardView((LEFT_COLUMN, BOARD_TOP), self.fonts, self.session.size)
        panel_rect = pygame.Rect(
            PANEL_LEFT,
            theme.MARGIN,
            theme.WINDOW_SIZE[0] - PANEL_LEFT - theme.MARGIN,
            theme.WINDOW_SIZE[1] - 2 * theme.MARGIN,
        )
        self.panel = SidePanel(panel_rect, self.fonts, self.t)
        self.image: ImageTiles | None = None
        self.notice: str | None = None
        self.running = True
        self._caption = None
        self._cursor = None

    def render(self, now_ms: int | None = None) -> None:
        now = pygame.time.get_ticks() if now_ms is None else now_ms
        session = self.session
        self.board.sync(session.state, session.won, now)
        self.screen.fill(theme.WALL)
        title_pos = (LEFT_COLUMN, theme.MARGIN - 8)
        draw.text(self.screen, self.fonts.title, self.t("title"), theme.COBALT, topleft=title_pos)
        self.board.draw(self.screen, session.state, self.image, now)
        self._draw_move_count()
        mouse = pygame.mouse.get_pos()
        self.panel.draw(self.screen, session, self.image, self.notice, mouse)

    def _draw_move_count(self) -> None:
        center_y = theme.WINDOW_SIZE[1] - theme.MARGIN - 32
        count = format_count(self.session.moves, self.t.language)
        label_pos = (LEFT_COLUMN, center_y)
        draw.text(self.screen, self.fonts.heading, self.t("moves"), theme.INK, midleft=label_pos)
        width = max(88, self.fonts.count.size(count)[0] + 36)
        plate_rect = pygame.Rect(0, 0, width, 64)
        plate_rect.midright = (self.board.rect.right, center_y)
        plate = draw.rounded(plate_rect.size, 10, theme.COBALT, theme.ENAMEL, 4)
        self.screen.blit(plate, plate_rect)
        draw.text(self.screen, self.fonts.count, count, theme.ENAMEL, center=plate_rect.center)

    def choose_image(self) -> None:
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title=self.t("dialog_title"),
            filetypes=[(self.t("dialog_filter"), "*.jpg;*.jpeg;*.png;*.bmp")],
        )
        root.destroy()
        if path:
            self.load_image(path)

    def load_image(self, path: str) -> None:
        try:
            self.image = ImageTiles(path)
        except (pygame.error, OSError, ValueError):
            self.notice = self.t("image_error")
            return
        self.session.shuffle()

    def set_language(self, language: str) -> None:
        self.t.language = language
        self.settings.language = language
        self.settings.save()

    def _run_action(self, action: str) -> None:
        session = self.session
        if action == "solve":
            if session.solving:
                session.cancel_solving()
            else:
                session.start_solving()
        elif action == "skip":
            session.skip_to_end()
        elif action == "shuffle":
            session.shuffle()
        elif action == "reset":
            session.reset()
        elif action == "choose":
            self.choose_image()
        elif action == "remove":
            self.image = None

    def _slide_cell(self, index: int) -> None:
        """Move the clicked plate if it is next to the blank."""
        session = self.session
        if session.solving or session.state[index] == BLANK:
            return
        for direction, next_state in neighbors(session.state):
            if next_state[index] == BLANK:
                session.move(direction)
                return

    def handle_click(self, pos) -> None:
        self.notice = None
        action = self.panel.action_at(pos)
        language = self.panel.language.hit(pos)
        algorithm = self.panel.algorithm_at(pos)
        cell = self.board.cell_at(pos)
        if action:
            self._run_action(action)
        elif language:
            self.set_language(language)
        elif algorithm and not self.session.solving:
            self.session.algorithm = algorithm
        elif cell is not None:
            self._slide_cell(cell)

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and not self.session.solving:
            if event.key in ARROW_MOVES:
                self.notice = None
                self.session.move(ARROW_MOVES[event.key])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def _update_window(self) -> None:
        player_won = self.session.won and not self.session.solved_by
        caption = self.t("title_won" if player_won else "title")
        if caption != self._caption:
            pygame.display.set_caption(caption)
            self._caption = caption
        mouse = pygame.mouse.get_pos()
        panel = self.panel
        clickable = (
            panel.action_at(mouse)
            or panel.language.hit(mouse)
            or (panel.algorithm_at(mouse) and not self.session.solving)
        )
        cursor = pygame.SYSTEM_CURSOR_HAND if clickable else pygame.SYSTEM_CURSOR_ARROW
        if cursor != self._cursor:
            pygame.mouse.set_cursor(cursor)
            self._cursor = cursor

    def run(self) -> None:
        while self.running:
            self.clock.tick(60)
            self.session.update(pygame.time.get_ticks())
            self.render()
            pygame.display.flip()
            self._update_window()
            for event in pygame.event.get():
                self.handle_event(event)
        pygame.quit()
