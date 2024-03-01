import pygame

from .drawnobject import DrawnObject
from .constants import WHITE


class Panel(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

    def update(self) -> None:
        self.x = self.x_padd + self.board_size + self.padd
        self.y = self.y_padd
        self.width = self.square_size
        self.height = self.board_size

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.rect(
            screen,
            WHITE,
            (self.x, self.y, self.width, self.height),
            self.line_size,
        )
