"""Game loop and event handling."""

from tkinter import Tk, filedialog, messagebox

import pygame

from npuzzle.core.session import GameSession
from npuzzle.ui import board_view, theme
from npuzzle.ui.image_tiles import ImageTiles
from npuzzle.ui.panels import ControlPanel

TITLE = "8 Puzzle Game"
ARROW_MOVES = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((theme.SCREEN_WIDTH, theme.SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fonts = theme.Fonts()
        self.session = GameSession()
        self.panel = ControlPanel(self.fonts)
        self.image: ImageTiles | None = None
        self.running = True

    def render(self) -> None:
        board_view.draw_background(self.screen)
        board_view.draw_board(
            self.screen, self.session.state, self.session.size, self.fonts, self.image
        )
        self.panel.draw(self.screen, self.session, self.image is not None)
        if self.image:
            board_view.draw_reference(self.screen, self.image, self.fonts)

    def choose_image(self) -> None:
        root = Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Chọn hình ảnh",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")],
        )
        root.destroy()
        if not path:
            return
        try:
            self.image = ImageTiles(path)
        except (pygame.error, OSError):
            root = Tk()
            root.withdraw()
            messagebox.showerror("Lỗi", "Không thể tải hình ảnh. Vui lòng chọn file hợp lệ.")
            root.destroy()
            return
        self.session.shuffle()

    def handle_click(self, pos) -> None:
        panel, session = self.panel, self.session
        if panel.buttons["shuffle"].collidepoint(pos) and not session.solving:
            session.shuffle()
        elif panel.buttons["choose"].collidepoint(pos):
            self.choose_image()
        elif panel.reset_rect.collidepoint(pos):
            session.reset()
        elif self.image and panel.trash_rect.collidepoint(pos):
            self.image = None
        elif panel.buttons["algorithm"].collidepoint(pos):
            panel.menu_open = not panel.menu_open
        elif panel.buttons["solve"].collidepoint(pos):
            if session.solving:
                session.cancel_solving()
            else:
                session.start_solving()
        elif panel.menu_open:
            for name, rect in panel.menu_options.items():
                if rect.collidepoint(pos):
                    session.algorithm = name
                    panel.menu_open = False
                    break

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
            caption = f"{TITLE} - YOU WIN!" if self.session.won else TITLE
            pygame.display.set_caption(caption)
            for event in pygame.event.get():
                self.handle_event(event)
        pygame.quit()
