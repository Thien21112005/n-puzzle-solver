"""Standard controls drawn in the enamel plate language."""

from dataclasses import dataclass

import pygame

from npuzzle.ui import draw, theme

_STYLES = {
    "primary": (theme.SHUTTER, theme.SHUTTER_DEEP, theme.ENAMEL, None),
    "secondary": (theme.COBALT, theme.COBALT_DEEP, theme.ENAMEL, None),
    "quiet": (theme.ENAMEL, theme.HOVER, theme.COBALT, theme.COBALT),
}


@dataclass
class Button:
    action: str
    rect: pygame.Rect
    label: str = ""
    style: str = "secondary"
    enabled: bool = True
    visible: bool = True

    def hit(self, pos) -> bool:
        return self.visible and self.enabled and self.rect.collidepoint(pos)

    def draw(self, screen, fonts: theme.Fonts, mouse) -> None:
        if not self.visible:
            return
        fill, hover, text_color, border = _STYLES[self.style]
        if not self.enabled:
            fill, text_color, border = theme.DISABLED_FILL, theme.DISABLED_TEXT, None
        elif self.rect.collidepoint(mouse):
            fill = hover
        width = 2 if border else 0
        surface = draw.rounded(self.rect.size, theme.CONTROL_RADIUS, fill, border, width)
        screen.blit(surface, self.rect)
        label = draw.fit_text(fonts.strong, self.label, self.rect.width - 16)
        draw.text(screen, fonts.strong, label, text_color, center=self.rect.center)


class Segmented:
    """A two-way switch; the selected side is filled."""

    def __init__(self, rect: pygame.Rect, options: dict[str, str]):
        self.rect = rect
        self.options = options
        width = rect.width // len(options)
        self.parts = {
            key: pygame.Rect(rect.x + index * width, rect.y, width, rect.height)
            for index, key in enumerate(options)
        }

    def hit(self, pos) -> str | None:
        for key, part in self.parts.items():
            if part.collidepoint(pos):
                return key
        return None

    def draw(self, screen, fonts: theme.Fonts, selected: str, mouse) -> None:
        outline = draw.rounded(self.rect.size, theme.CONTROL_RADIUS, theme.ENAMEL, theme.COBALT, 2)
        screen.blit(outline, self.rect)
        for key, part in self.parts.items():
            active = key == selected
            if active:
                fill = draw.rounded(part.size, theme.CONTROL_RADIUS, theme.COBALT)
                screen.blit(fill, part)
            elif part.inflate(-6, -6).collidepoint(mouse):
                hover = draw.rounded(part.inflate(-6, -6).size, 5, theme.HOVER)
                screen.blit(hover, part.inflate(-6, -6))
            color = theme.ENAMEL if active else theme.COBALT
            draw.text(screen, fonts.strong, self.options[key], color, center=part.center)
