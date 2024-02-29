import pygame

from engine.board import Board
from gui.panel import Panel
from gui.drawnobject import DrawnObject
from gui.constants import WHITE, BLUE


class Game(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

        self.board = Board()
        self.panel = Panel()

        self.player_is_white = True
        self.white_pov = self.player_is_white

    def update(self) -> None:
        # reload and resize image on window size changes
        self.load_images()

    def get_x(self, col: int | float) -> int:
        return round(self.x_padd + self.square_size * col)

    def get_y(self, row: int | float) -> int:
        return round(self.y_padd + self.square_size * row)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(WHITE)
        self.panel.draw(screen)

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

        # draw each piece
        for pos in range(120):
            # get the piece, rank, and file
            piece = self.board.board[pos]
            rank = pos // 10 - 2
            file = pos % 10 - 1

            if piece not in " .":
                screen.blit(self.images[piece], (self.get_x(file), self.get_y(rank)))

    def load_images(self) -> None:
        # load each piece where the key is the char stored in the board
        self.images = {
            "P": pygame.image.load("assets/white-pawn.png"),
            "N": pygame.image.load("assets/white-knight.png"),
            "B": pygame.image.load("assets/white-bishop.png"),
            "R": pygame.image.load("assets/white-rook.png"),
            "Q": pygame.image.load("assets/white-queen.png"),
            "K": pygame.image.load("assets/white-king.png"),
            "p": pygame.image.load("assets/black-pawn.png"),
            "n": pygame.image.load("assets/black-knight.png"),
            "b": pygame.image.load("assets/black-bishop.png"),
            "r": pygame.image.load("assets/black-rook.png"),
            "q": pygame.image.load("assets/black-queen.png"),
            "k": pygame.image.load("assets/black-king.png"),
        }

        # resize each image to square_size
        for name, image in self.images.items():
            self.images[name] = pygame.transform.smoothscale(
                image, (self.square_size, self.square_size)
            )
