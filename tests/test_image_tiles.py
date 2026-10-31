import pygame

from npuzzle.ui.image_tiles import ImageTiles

GREEN = (0, 255, 0)
RED = (255, 0, 0)


def assert_close(pixel, expected):
    """Allow for the small rounding smoothscale introduces."""
    assert all(abs(a - b) <= 4 for a, b in zip(pixel[:3], expected, strict=True)), pixel


def test_wide_picture_is_center_cropped(display, tmp_path):
    picture = pygame.Surface((300, 100))
    picture.fill(RED)
    picture.fill(GREEN, (100, 0, 100, 100))
    path = tmp_path / "wide.png"
    pygame.image.save(picture, path)

    image = ImageTiles(str(path))

    width, height = image.reference.get_size()
    for x, y in [(12, 12), (width - 13, 12), (12, height - 13), (width - 13, height - 13)]:
        assert_close(image.reference.get_at((x, y)), GREEN)


def test_palette_picture_can_be_loaded(display, tmp_path):
    picture = pygame.Surface((90, 90), depth=8)
    picture.set_palette_at(0, RED)
    path = tmp_path / "palette.bmp"
    pygame.image.save(picture, path)

    assert_close(ImageTiles(str(path)).reference.get_at((40, 40)), RED)
