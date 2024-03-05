import pygame

import engine
import utils
from .heldpiece import HeldPiece
from .drawnobject import DrawnObject
from .constants import LIGHT, DARK


class Board(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

    def update(self) -> None:
        # reload and resize image on window size changes
        self.load_images()

    def get_x(self, col: int | float) -> int:
        return round(self.x_padd + self.square_size * col)

    def get_y(self, row: int | float) -> int:
        return round(self.y_padd + self.square_size * row)

    def draw(
        self,
        screen: pygame.surface.Surface,
        board: engine.Board,
        white_pov: bool,
        held_piece: HeldPiece,
        x_offset: int,
        y_offset: int,
    ) -> None:
        # draw each piece
        for pos in range(120):
            # get the piece, rank, and file
            piece = board.board[pos]
            rank = pos // 10 - 2
            file = pos % 10 - 1

            # flip the rank and file if black's pov
            rank, file = utils.flip_coordinates(rank, file, white_pov)

            if not piece.isspace():
                # draw the square
                pygame.draw.rect(
                    screen,
                    LIGHT if (rank + file) % 2 == 0 else DARK,
                    (
                        self.get_x(file),
                        self.get_y(rank),
                        self.square_size,
                        self.square_size,
                    ),
                )

            # draw piece
            if piece.isalpha() and (rank, file) != (held_piece.rank, held_piece.file):
                screen.blit(
                    self.images[piece],
                    (
                        self.get_x(file) + self.line_size,
                        self.get_y(rank) + self.line_size,
                    ),
                )

        # draw held piece
        if held_piece.piece:
            x, y = pygame.mouse.get_pos()
            screen.blit(
                self.images[held_piece.piece],
                (x - x_offset, y - y_offset),
            )

        # draw board border
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.x_padd, self.y_padd, self.board_size, self.board_size),
            self.line_size,
        )

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
                image, (self.piece_size, self.piece_size)
            )
