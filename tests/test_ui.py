import pygame
import pytest

from npuzzle.app import App


@pytest.fixture
def app():
    instance = App()
    yield instance
    pygame.quit()


def test_app_renders_from_another_working_directory(app, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    App().render()


def test_click_outside_closes_the_algorithm_menu(app):
    app.handle_click(app.panel.buttons["algorithm"].center)
    assert app.panel.menu_open
    app.handle_click((5, 5))
    assert not app.panel.menu_open


def test_algorithm_button_toggles_the_menu(app):
    button = app.panel.buttons["algorithm"].center
    app.handle_click(button)
    app.handle_click(button)
    assert not app.panel.menu_open


def test_choosing_a_menu_option_selects_the_algorithm(app):
    app.handle_click(app.panel.buttons["algorithm"].center)
    app.handle_click(app.panel.menu_options["A*"].center)
    assert app.session.algorithm == "A*"
    assert not app.panel.menu_open
