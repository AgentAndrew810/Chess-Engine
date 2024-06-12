import pygame

from .constants import WHITE


class MenuButton:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, colour: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        self.text = text

        self.colour = colour
        self.darkened_colour = (round(colour[0] * 0.65), round(colour[1] * 0.65), round(colour[2] * 0.65))

    def is_over(self) -> bool:
        x, y = pygame.mouse.get_pos()

        # determine if the mouse position is within the button
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                return True

        return False

    def draw(self, screen: pygame.surface.Surface, font: pygame.font.Font) -> None:
        # draw the button
        pygame.draw.rect(screen, self.darkened_colour if self.is_over() else self.colour, self.rect, 0, min(self.width, self.height) // 2)

        # draw text on button
        text = font.render(self.text, True, WHITE)
        rect = text.get_rect(center=self.rect.center)
        screen.blit(text, rect)
