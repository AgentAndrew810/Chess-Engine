import pygame
from math import sqrt

from .constants import WHITE, BLACK, BLUE


class RadioButton:
    def __init__(self, center: tuple[int, int], radius: int, text: str, enabled: bool) -> None:
        self.resize(center, radius)
        self.text = text
        self.enabled = enabled

    def resize(self, center: tuple[int, int], radius: int) -> None:
        self.center = center
        self.radius = radius

    def is_over(self) -> bool:
        x, y = pygame.mouse.get_pos()
        distance = sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2)

        # determine if the mouse position is within the button
        if distance <= self.radius:
            return True

        return False

    def draw(self, screen: pygame.surface.Surface, font: pygame.font.Font) -> None:
        # draw the button filled in if it is selected
        if self.enabled:
            pygame.draw.circle(screen, BLUE, self.center, round(self.radius * 1.2) if self.is_over() else self.radius)

        # draw the button outline
        pygame.draw.circle(screen, BLACK, self.center, round(self.radius * 1.2) if self.is_over() else self.radius, round(self.radius / 6))

        # draw text after button
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.center[0] + round(self.radius * 1.75), self.center[1] - text.get_height() // 2))
