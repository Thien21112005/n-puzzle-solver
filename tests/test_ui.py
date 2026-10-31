import pygame

from npuzzle.app import App


def test_app_renders_from_another_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app = App()
    app.render()
    pygame.quit()
