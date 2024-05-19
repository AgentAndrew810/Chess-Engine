import pygame

from engine import Board, Move
from .drawnobject import DrawnObject
from .utils import draw_transparent_object
from .constants import WHITE, BLACK


class Panel(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

    def update(self) -> None:
        # deteremine panel sizes
        panel_x = self.board_end_x + self.unit // 2
        panel_y = self.board_start_y
        panel_width = self.unit * 5

        self.info_pos = (panel_x, panel_y)
        self.info_size = (panel_width, round(self.unit * 0.75))

        self.white_clock_pos = (panel_x, panel_y + round(self.unit * 0.75))
        self.white_clock_size = (panel_width // 2, self.unit)
        self.black_clock_pos = (panel_x + panel_width // 2, panel_y + round(self.unit * 0.75))
        self.black_clock_size = (panel_width // 2, self.unit)

        self.moves_pos = (panel_x, panel_y + round(self.unit * 1.75))
        self.moves_size = (panel_width, round(self.unit * 5.75))

    def draw(self, screen: pygame.surface.Surface, board: Board, past_moves: list[Move]) -> None:
        draw_transparent_object(screen, BLACK, self.info_pos, self.info_size, 200)
        draw_transparent_object(screen, WHITE, self.white_clock_pos, self.white_clock_size, 255)
        draw_transparent_object(screen, BLACK, self.black_clock_pos, self.black_clock_size, 255)
        draw_transparent_object(screen, BLACK, self.moves_pos, self.moves_size, 200)
