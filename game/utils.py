import pygame


def get_pos(rank: int, file: int, white_pov: bool = True) -> int:
    rank, file = (rank, file) if white_pov else (7 - rank, 7 - file)
    return (rank + 2) * 10 + file + 1


def draw_transparent_object(
    screen: pygame.surface.Surface, colour: tuple[int, int, int], position: tuple[int, int], size: tuple[int, int], alpha: int
):
    s = pygame.Surface(size)
    s.set_alpha(alpha)
    s.fill(colour)
    screen.blit(s, position)
