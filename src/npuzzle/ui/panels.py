"""The white enamel panel: comparison table, status, actions, picture and language."""

import pygame

from npuzzle.core.session import GameSession, RunRecord
from npuzzle.core.solvers import ALGORITHMS
from npuzzle.i18n import LANGUAGE_NAMES, Translator, format_bytes, format_count, format_seconds
from npuzzle.ui import draw, theme
from npuzzle.ui.image_tiles import REFERENCE_SIZE, ImageTiles
from npuzzle.ui.widgets import Button, Segmented

PADDING = 3 * theme.UNIT
ROW_HEIGHT = 44
HEADER_HEIGHT = 32
RADIO_RADIUS = 7
# Right edge of each column measured from the table's left, and how each one is read and shown.
COLUMNS = (
    ("col_nodes", 196, lambda r: r.nodes, lambda r, lang: format_count(r.nodes, lang)),
    ("col_steps", 272, lambda r: r.steps, lambda r, lang: format_count(r.steps, lang)),
    ("col_time", 364, lambda r: r.seconds, lambda r, lang: format_seconds(r.seconds, lang)),
    (
        "col_memory",
        512,
        lambda r: r.memory_estimate,
        lambda r, lang: format_bytes(r.memory_estimate, lang),
    ),
)


class SidePanel:
    def __init__(self, rect: pygame.Rect, fonts: theme.Fonts, t: Translator):
        self.rect = rect
        self.fonts = fonts
        self.t = t
        left, top = rect.x + PADDING, rect.y + PADDING
        self.inner_width = rect.width - 2 * PADDING
        self.table_top = top + 40
        self.table_x = left
        self.rows = {
            name: pygame.Rect(
                left, self.table_top + HEADER_HEIGHT + i * ROW_HEIGHT, self.inner_width, ROW_HEIGHT
            )
            for i, name in enumerate(ALGORITHMS)
        }
        table_bottom = self.table_top + HEADER_HEIGHT + len(ALGORITHMS) * ROW_HEIGHT
        self.note_y = table_bottom + 8
        self.status_rect = pygame.Rect(left, self.note_y + 32, self.inner_width, 32)

        y = self.status_rect.bottom + 12
        h = theme.CONTROL_HEIGHT
        self.solve = Button("solve", pygame.Rect(left, y, 196, h), style="primary")
        self.skip = Button("skip", pygame.Rect(left + 204, y, 96, h), style="quiet")
        self.shuffle = Button("shuffle", pygame.Rect(left + 308, y, 104, h), style="quiet")
        self.reset = Button("reset", pygame.Rect(left + 420, y, 104, h), style="quiet")

        self.picture_y = y + h + 40
        text_x = left + REFERENCE_SIZE + 16
        button_y = self.picture_y + REFERENCE_SIZE - h
        self.choose = Button("choose", pygame.Rect(text_x, button_y, 192, h), style="quiet")
        self.remove = Button("remove", pygame.Rect(text_x + 104, button_y, 88, h), style="quiet")
        self.buttons = [self.solve, self.skip, self.shuffle, self.reset, self.choose, self.remove]
        language_rect = pygame.Rect(left + self.inner_width - 192, button_y, 192, h)
        self.language = Segmented(language_rect, LANGUAGE_NAMES)

    def _update_controls(self, session: GameSession, image: ImageTiles | None) -> None:
        t = self.t
        self.solve.label = (
            t("cancel") if session.solving else t("solve_with", algorithm=session.algorithm)
        )
        self.solve.style = "quiet" if session.solving else "primary"
        self.solve.enabled = session.solving or not session.won or bool(session.solved_by)
        self.skip.label = t("skip")
        self.skip.enabled = bool(session.solution)
        self.shuffle.label = t("shuffle")
        self.shuffle.enabled = not session.solving
        # After the player wins, starting a new game is the obvious next step.
        player_won = session.won and not session.solved_by
        self.shuffle.style = "secondary" if player_won else "quiet"
        self.reset.label = t("reset")
        self.choose.label = t("change_image") if image else t("choose_image")
        self.choose.rect.width = 96 if image else 192  # Shares the row with Remove.
        self.remove.label = t("remove_image")
        self.remove.visible = image is not None

    def action_at(self, pos) -> str | None:
        for button in self.buttons:
            if button.hit(pos):
                return button.action
        return None

    def focus_targets(self, session: GameSession) -> list[pygame.Rect]:
        """Return the controls reachable with Tab, in reading order."""
        rows = [] if session.solving else list(self.rows.values())
        buttons = [b.rect for b in self.buttons if b.visible and b.enabled]
        return rows + buttons + list(self.language.parts.values())

    def algorithm_at(self, pos) -> str | None:
        for name, row in self.rows.items():
            if row.collidepoint(pos):
                return name
        return None

    def _draw_table(self, screen, session: GameSession, mouse) -> None:
        fonts, t = self.fonts, self.t
        header_y = self.table_top + HEADER_HEIGHT // 2
        draw.text(
            screen, fonts.strong, t("col_algorithm"), theme.INK, midleft=(self.table_x, header_y)
        )
        for key, right, _, _ in COLUMNS:
            draw.text(
                screen, fonts.strong, t(key), theme.INK, midright=(self.table_x + right, header_y)
            )
        records = session.comparison()
        best = {}
        if len(records) > 1:
            best = {key: min(read(r) for r in records.values()) for key, _, read, _ in COLUMNS}
        for name, row in self.rows.items():
            self._draw_row(screen, session, name, row, records.get(name), best, mouse)
        rule_y = self.table_top + HEADER_HEIGHT - 1
        x_end = self.table_x + self.inner_width
        pygame.draw.line(screen, theme.COBALT, (self.table_x, rule_y), (x_end, rule_y), 2)

    def _draw_row(self, screen, session, name, row, record: RunRecord | None, best, mouse) -> None:
        fonts = self.fonts
        selected = name == session.algorithm
        background = theme.ENAMEL
        if selected:
            background = theme.SELECTED
        elif row.collidepoint(mouse) and not session.solving:
            background = theme.HOVER
        if background != theme.ENAMEL:
            screen.blit(draw.rounded(row.size, 6, background), row)
        radio = (row.x + 16, row.centery)
        draw.dot(screen, radio, RADIO_RADIUS, theme.COBALT)
        draw.dot(screen, radio, RADIO_RADIUS - 2, background)
        if selected:
            draw.dot(screen, radio, RADIO_RADIUS - 4, theme.COBALT)
        draw.text(screen, fonts.strong, name, theme.INK, midleft=(row.x + 32, row.centery))
        pygame.draw.line(screen, theme.RULE, (row.x, row.bottom - 1), (row.right, row.bottom - 1))
        for key, right, read, show in COLUMNS:
            x = self.table_x + right
            if record is None:
                draw.tabular_text(screen, fonts.data, "—", theme.INK_SOFT, x, row.centery)
                continue
            is_best = key in best and read(record) == best[key]
            value = show(record, self.t.language)
            if is_best:
                # Bold digits look split in equal-width cells, and the weight marks them anyway.
                midright = (x, row.centery)
                draw.text(screen, fonts.data_best, value, theme.SHUTTER, midright=midright)
            else:
                draw.tabular_text(screen, fonts.data, value, theme.INK, x, row.centery)

    def _status(self, session: GameSession, notice: str | None) -> tuple[str, tuple]:
        t = self.t
        if notice:
            return notice, theme.ERROR
        if session.searching:
            return t("searching", algorithm=session.algorithm), theme.COBALT
        if session.solving:
            count = t.moves(len(session.solution))
            return t("playing", algorithm=session.algorithm, count=count), theme.COBALT
        if session.no_solution:
            return t("no_solution", algorithm=session.algorithm), theme.ERROR
        if session.won:
            count = t.moves(session.moves)
            if session.solved_by:
                return t("solved", algorithm=session.solved_by, count=count), theme.SHUTTER
            return t("won", count=count), theme.SHUTTER
        return t("hint"), theme.INK_SOFT

    def _draw_number_preview(self, screen, frame: pygame.Rect) -> None:
        """Show the finished board, which is the goal while no picture is loaded."""
        screen.blit(draw.rounded(frame.size, theme.CONTROL_RADIUS, theme.ENAMEL_SHADE), frame)
        cell, gap = 24, 4
        start_x = frame.x + (frame.width - 3 * cell - 2 * gap) // 2
        start_y = frame.y + (frame.height - 3 * cell - 2 * gap) // 2
        plate = draw.rounded((cell, cell), 4, theme.COBALT)
        for index in range(8):
            row, col = divmod(index, 3)
            position = pygame.Rect(
                start_x + col * (cell + gap), start_y + row * (cell + gap), cell, cell
            )
            screen.blit(plate, position)
            number = str(index + 1)
            draw.text(screen, self.fonts.small_bold, number, theme.ENAMEL, center=position.center)

    def _draw_picture(self, screen, image: ImageTiles | None) -> None:
        fonts, t = self.fonts, self.t
        x, y = self.table_x, self.picture_y
        frame = pygame.Rect(x, y, REFERENCE_SIZE, REFERENCE_SIZE)
        text_x = frame.right + 16
        if image:
            screen.blit(image.reference, frame)
        else:
            self._draw_number_preview(screen, frame)
        title = t("picture_on") if image else t("picture_off")
        detail = t("reference") if image else t("reference_board")
        draw.text(screen, fonts.strong, title, theme.INK, topleft=(text_x, y))
        draw.text(screen, fonts.small, detail, theme.INK_SOFT, topleft=(text_x, y + 22))
        label = (self.language.rect.x, y)
        draw.text(screen, fonts.strong, t("language"), theme.INK, topleft=label)

    def draw(self, screen, session, image, notice: str | None, mouse) -> None:
        self._update_controls(session, image)
        fonts, t = self.fonts, self.t
        shadow = draw.soft_shadow(self.rect.size, theme.PANEL_RADIUS, 70)
        screen.blit(shadow, self.rect.move(-8, -4))
        screen.blit(draw.rounded(self.rect.size, theme.PANEL_RADIUS, theme.ENAMEL), self.rect)
        heading_pos = (self.table_x, self.rect.y + PADDING)
        draw.text(screen, fonts.heading, t("comparison"), theme.COBALT, topleft=heading_pos)
        self._draw_table(screen, session, mouse)
        note_pos = (self.table_x, self.note_y)
        note = t("table_note") if session.comparison() else t("table_empty")
        draw.text(screen, fonts.small, note, theme.INK_SOFT, topleft=note_pos)

        message, color = self._status(session, notice)
        message = draw.fit_text(fonts.strong, message, self.status_rect.width)
        draw.text(screen, fonts.strong, message, color, midleft=self.status_rect.midleft)
        for button in self.buttons:
            button.draw(screen, fonts, mouse)
        rule_y = self.picture_y - 20
        pygame.draw.line(
            screen, theme.RULE, (self.table_x, rule_y), (self.table_x + self.inner_width, rule_y)
        )
        self._draw_picture(screen, image)
        self.language.draw(screen, fonts, t.language, mouse)
