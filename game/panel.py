import pygame

from .drawnobject import DrawnObject
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

        self.info_size = (panel_width, self.unit * 0.75)
        self.info_pos = (panel_x, panel_y)

        self.white_clock_size = (panel_width // 2, self.unit)
        self.white_clock_pos = (panel_x, panel_y + self.unit * 0.75)
        self.black_clock_size = (panel_width // 2, self.unit)
        self.black_clock_pos = (panel_x + panel_width // 2, panel_y + self.unit * 0.75)
        
        self.moves_size = ()

    def draw(self, screen: pygame.surface.Surface) -> None:
        # draw the info bar
        s = pygame.Surface(self.info_size)
        s.set_alpha(200)
        s.fill(BLACK)
        screen.blit(s, self.info_pos)

        # draw the clocks
        s = pygame.Surface(self.white_clock_size)
        s.set_alpha(200)
        s.fill(WHITE)
        screen.blit(s, self.white_clock_pos)

        s = pygame.Surface(self.black_clock_size)
        s.set_alpha(200)
        s.fill(BLACK)
        screen.blit(s, self.black_clock_pos)
        
        # moves played
        
