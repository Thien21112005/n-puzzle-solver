"""Game loop and event handling."""

from tkinter import Tk, filedialog, messagebox

import pygame

from npuzzle.core.session import GameSession
from npuzzle.i18n import Translator
from npuzzle.settings import Settings
from npuzzle.ui import board_view, theme
from npuzzle.ui.image_tiles import ImageTiles
from npuzzle.ui.panels import ControlPanel

ARROW_MOVES = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


class App:
    def __init__(self):
        pygame.init()
        self.settings = Settings.load()
        self.t = Translator(self.settings.language)
        self.screen = pygame.display.set_mode((theme.SCREEN_WIDTH, theme.SCREEN_HEIGHT))
        pygame.display.set_caption(self.t("title"))
        self.clock = pygame.time.Clock()
        self.fonts = theme.Fonts()
        self.session = GameSession()
        self.panel = ControlPanel(self.fonts, self.t)
        self.image: ImageTiles | None = None
        self.running = True

    def render(self) -> None:
        board_view.draw_background(self.screen)
        board_view.draw_board(
            self.screen, self.session.state, self.session.size, self.fonts, self.image
        )
        self.panel.draw(self.screen, self.session, self.image is not None)
        if self.image:
            board_view.draw_reference(self.screen, self.image, self.fonts, self.t("reference"))

    def choose_image(self) -> None:
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title=self.t("dialog_title"),
            filetypes=[(self.t("dialog_filter"), "*.jpg;*.jpeg;*.png;*.bmp")],
        )
        root.destroy()
        if not path:
            return
        try:
            self.image = ImageTiles(path)
        except (pygame.error, OSError):
            root = Tk()
            root.withdraw()
            messagebox.showerror(self.t("error_title"), self.t("image_error"))
            root.destroy()
            return
        self.session.shuffle()

    def handle_click(self, pos) -> None:
        panel, session = self.panel, self.session
        if panel.menu_open:
            panel.menu_open = False
            for name, rect in panel.menu_options.items():
                if rect.collidepoint(pos):
                    session.algorithm = name
                    return
            if panel.buttons["algorithm"].collidepoint(pos):
                return
        if panel.buttons["shuffle"].collidepoint(pos) and not session.solving:
            session.shuffle()
        elif panel.buttons["choose"].collidepoint(pos):
            self.choose_image()
        elif panel.reset_rect.collidepoint(pos):
            session.reset()
        elif self.image and panel.trash_rect.collidepoint(pos):
            self.image = None
        elif panel.buttons["algorithm"].collidepoint(pos) and not session.solving:
            panel.menu_open = True
        elif panel.skip_rect.collidepoint(pos) and session.solution:
            session.skip_to_end()
        elif panel.buttons["solve"].collidepoint(pos):
            if session.solving:
                session.cancel_solving()
            else:
                session.start_solving()

    def handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and not self.session.solving:
            if event.key in ARROW_MOVES:
                self.session.move(ARROW_MOVES[event.key])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def run(self) -> None:
        while self.running:
            self.clock.tick(60)
            self.render()
            pygame.display.flip()
            self.session.update(pygame.time.get_ticks())
            pygame.display.set_caption(self.t("title_won" if self.session.won else "title"))
            for event in pygame.event.get():
                self.handle_event(event)
        pygame.quit()
