import pygame


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, file: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        size = round(min(width, height) * 0.6)

        self.x_pos = x + (width - size) // 2
        self.y_pos = y + (height - size) // 2

        self.image = pygame.image.load(file)
        self.image = pygame.transform.smoothscale(self.image, (size, size))

    def is_over(self) -> bool:
        return False

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, (self.x_pos, self.y_pos))
