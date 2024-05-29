import pygame


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, file: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        size = round(min(width, height) * 0.6)
        big_size = round(min(width, height) * 0.7)

        self.location = (x + (width - size) // 2, y + (height - size) // 2)
        self.big_location = (x + (width - big_size) // 2, y + (height - big_size) // 2)

        self.image = pygame.transform.smoothscale(pygame.image.load(file), (size, size))
        self.big_image = pygame.transform.smoothscale(pygame.image.load(file), (big_size, big_size))

    def is_over(self) -> bool:
        x, y = pygame.mouse.get_pos()

        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.width:
                return True

        return False

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.is_over():
            screen.blit(self.big_image, self.big_location)
        else:
            screen.blit(self.image, self.location)
