import pygame

from .constants import BLACK, WHITE, BLUE
from .drawnobject import DrawnObject


class Game(DrawnObject):
    def __init__(self) -> None:
        pass

    def get_x(self, col: int | float) -> int:
        return round(
            self.x_padd + self.square_size * 3 + self.padd + self.square_size * col
        )

    def get_y(self, row: int | float) -> int:
        return round(
            self.y_padd + self.square_size + self.padd + self.square_size * row
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(BLACK)

        # draw the checkerboard
        for rank in range(8):
            for file in range(8):
                colour = WHITE if (rank + file) % 2 == 0 else BLUE

                # draw the square
                pygame.draw.rect(
                    screen,
                    colour,
                    (
                        self.get_x(file),
                        self.get_y(rank),
                        self.square_size,
                        self.square_size,
                    ),
                )
