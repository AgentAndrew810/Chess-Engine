import pygame

from utils import darken
from .drawnobject import DrawnObject


class Button(DrawnObject):
    def __init__(self, x: int, y: int, colour: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y

        self.colour = colour
        self.edge = darken(colour, 0.5)
        self.hover = darken(colour, 0.6)
        self.edge_hover = darken(self.edge, 0.6)

    def is_over(self):
        x, y = pygame.mouse.get_pos()
        if self.x <= x <= self.x + self.square_size:
            if self.y <= y <= self.y + self.square_size:
                return True

        return False

    def draw(self, screen: pygame.surface.Surface) -> None:
        colour, edge = (
            (self.hover, self.edge_hover)
            if self.is_over()
            else (self.colour, self.edge)
        )

        # draw inside
        pygame.draw.rect(
            screen, colour, (self.x, self.y, self.square_size, self.square_size)
        )

        # draw outline
        pygame.draw.rect(
            screen,
            edge,
            (self.x, self.y, self.square_size, self.square_size),
            self.line_size,
        )
