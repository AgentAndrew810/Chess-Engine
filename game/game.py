import pygame

from .constants import BLACK
from .drawnobject import DrawnObject


class Game(DrawnObject):
    def __init__(self) -> None:
        pass

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(BLACK)
