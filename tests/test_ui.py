import pygame
import pytest

from npuzzle.app import App
from npuzzle.core.board import apply_move, goal_state
from npuzzle.core.solvers import ALGORITHMS
from npuzzle.i18n import STRINGS, Translator, format_bytes, format_count, format_seconds
from npuzzle.settings import Settings

ONE_MOVE_AWAY = apply_move(goal_state(3), "down")


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr("npuzzle.settings.default_settings_path", lambda: tmp_path / "s.json")
    instance = App()
    yield instance
    pygame.quit()


def place(app, state):
    app.session.state = state
    app.session.initial_state = state
    app.session.moves = 0


def test_app_renders_from_another_working_directory(app, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    App().render()


def test_clicking_a_row_selects_the_algorithm(app):
    app.handle_click(app.panel.rows["A*"].center)
    assert app.session.algorithm == "A*"


def test_clicking_a_plate_next_to_the_blank_moves_it(app):
    place(app, ONE_MOVE_AWAY)  # blank at index 5, tile 6 at index 8
    app.handle_click(app.board.cell_position(8))
    assert app.session.state == goal_state(3)
    assert app.session.moves == 1


def test_clicking_a_far_plate_does_nothing(app):
    place(app, ONE_MOVE_AWAY)
    app.handle_click(app.board.cell_position(0))
    assert app.session.moves == 0


def test_language_switch_is_saved(app):
    app.handle_click(app.panel.language.parts["en"].center)
    assert app.t.language == "en"
    assert Settings.load().language == "en"


def test_bad_image_shows_a_notice_and_keeps_the_board(app, tmp_path):
    bad = tmp_path / "bad.png"
    bad.write_text("not a picture")
    board = app.session.state
    app.load_image(str(bad))
    assert app.notice == app.t("image_error")
    assert app.session.state == board
    app.handle_click((1, 1))
    assert app.notice is None


@pytest.mark.parametrize("language", STRINGS)
def test_labels_fit_their_controls(app, language):
    app.t.language = language
    panel, fonts = app.panel, app.fonts
    t = Translator(language)
    longest_algorithm = max(ALGORITHMS, key=len)
    labels = [
        (panel.solve, [t("solve_with", algorithm=longest_algorithm), t("cancel")]),
        (panel.skip, [t("skip")]),
        (panel.shuffle, [t("shuffle")]),
        (panel.reset, [t("reset")]),
        (panel.choose, [t("choose_image"), t("change_image")]),
        (panel.remove, [t("remove_image")]),
    ]
    for button, texts in labels:
        for text in texts:
            assert fonts.strong.size(text)[0] <= button.rect.width - 16, text
    for key in ("hint", "image_error", "playing", "searching", "won", "solved", "no_solution"):
        text = STRINGS[language][key].format(algorithm=longest_algorithm, count="55.000")
        assert fonts.strong.size(text)[0] <= panel.status_rect.width, text
    assert fonts.small.size(t("table_note"))[0] <= panel.inner_width
    assert fonts.small.size(t("table_empty"))[0] <= panel.inner_width
    assert fonts.small.size(t("picture_hint"))[0] <= panel.language.rect.x - panel.choose.rect.x - 8


def test_number_formats_follow_the_language():
    assert format_count(176265, "vi") == "176.265"
    assert format_count(176265, "en") == "176,265"
    assert format_seconds(0.39, "vi") == "390 ms"
    assert format_seconds(1.5, "vi") == "1,50 s"
    assert format_seconds(1.5, "en") == "1.50 s"
    assert format_seconds(0.004, "en") == "4.0 ms"
    assert format_bytes(2400, "en") == "≈ 2 KB"
    assert format_bytes(21 * 1024 * 1024, "vi") == "≈ 21,0 MB"
