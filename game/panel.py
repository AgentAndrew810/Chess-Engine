import pygame

from .drawnobject import DrawnObject
from .constants import DARK, DARK_GREY, GREY, WHITE


class Panel(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

    def update(self) -> None:
        # size and position for the info bar
        self.info_rect = pygame.rect.Rect(
            (self.x_padd + self.unit * 9, self.y_padd, self.unit * 5, self.unit),
        )

        # size and position for the clocks
        self.white_clock_rect = pygame.rect.Rect(
            (self.x_padd + self.unit * 9, self.y_padd + self.unit, round(self.unit * 2.5), round(self.unit * 1.25))
        )
        self.black_clock_rect = pygame.rect.Rect(
            (self.x_padd + round(self.unit * 11.5), self.y_padd + self.unit, round(self.unit * 2.5), round(self.unit * 1.25))
        )

        # size and position for the move list
        self.move_rect = pygame.rect.Rect((self.x_padd + self.unit * 9, self.y_padd + round(self.unit * 2.25), self.unit * 5, self.unit * 5))

        # size and position for the bottom bar
        self.bottom_rect = pygame.rect.Rect(
            (self.x_padd + self.unit * 9, self.y_padd + round(self.unit * 7.25), self.unit * 5, round(self.unit * 0.75))
        )

        self.clock_font = pygame.font.Font("assets/OpenSans.ttf", round(self.unit * 0.5))
        self.info_font = pygame.font.Font("assets/OpenSans.ttf", round(self.unit * 0.36))

        self.pfp_size = round(self.unit * 0.6)
        self.pfp_image = pygame.image.load("assets/pfp.png")
        self.pfp_image = pygame.transform.smoothscale(self.pfp_image, (self.pfp_size, self.pfp_size))

    def draw(self, screen: pygame.surface.Surface, wtime: float, btime: float, info: str) -> None:
        self.draw_alpha_rect(screen, DARK, self.info_rect, self.unit // 10, self.unit // 10)
        self.draw_alpha_rect(screen, WHITE, self.white_clock_rect)
        self.draw_alpha_rect(screen, DARK_GREY, self.black_clock_rect)
        self.draw_alpha_rect(screen, GREY, self.move_rect)
        self.draw_alpha_rect(screen, WHITE, self.bottom_rect, 0, 0, self.unit // 10, self.unit // 10)

        # calculate time
        wmin, wsec = divmod(int(wtime), 60)
        bmin, bsec = divmod(int(btime), 60)

        # get white clock
        wtext = self.clock_font.render(f"{wmin:02}:{wsec:02}", True, DARK)
        wtext_rect = wtext.get_rect(center=self.white_clock_rect.center)
        screen.blit(wtext, wtext_rect)

        # get black clock
        btext = self.clock_font.render(f"{bmin:02}:{bsec:02}", True, DARK)
        btext_rect = btext.get_rect(center=self.black_clock_rect.center)
        screen.blit(btext, btext_rect)

        # draw info bar
        info_text = self.info_font.render(info, True, WHITE)
        info_text_rect = info_text.get_rect(center=self.info_rect.center)
        screen.blit(info_text, info_text_rect)

        screen.blit(self.pfp_image, (self.unit * 3, self.unit))

    def draw_alpha_rect(
        self,
        screen: pygame.surface.Surface,
        colour: tuple[int, int, int] | tuple[int, int, int, int],
        rect: pygame.Rect,
        top_left: int = 0,
        top_right: int = 0,
        bottom_left: int = 0,
        bottom_right: int = 0,
    ) -> None:
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            s,
            colour,
            s.get_rect(),
            border_top_left_radius=top_left,
            border_top_right_radius=top_right,
            border_bottom_left_radius=bottom_left,
            border_bottom_right_radius=bottom_right,
        )
        screen.blit(s, rect)
