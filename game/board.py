import pygame

import engine
import utils
from .heldpiece import HeldPiece
from .drawnobject import DrawnObject
from .constants import WHITE, BLUE, PINK, DARK_PINK


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
        last_move: engine.Move,
        x_offset: int,
        y_offset: int,
    ) -> None:
        for rank in range(8):
            for file in range(8):
                # get the pos and piece
                pos = utils.get_pos(rank, file, white_pov)
                piece = board.board[pos]

                # draw background square
                if piece not in " ":
                    colour = WHITE if (rank + file) % 2 == 0 else BLUE

                    # colour the squares involved in the past move
                    if pos in (last_move.pos, last_move.dest):
                        colour = PINK

                        # change colour of past move position if the move was one square over
                        dist = abs(last_move.pos - last_move.dest)
                        if dist in (1, 10) and pos == last_move.pos:
                            colour = DARK_PINK

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

                # draw the piece
                if piece not in " ." and pos != held_piece.pos:
                    screen.blit(
                        self.images[piece],
                        (
                            self.get_x(file) + self.line_size,
                            self.get_y(rank) + self.line_size,
                        ),
                    )

                if pos in held_piece.moves:
                    # determine the radius and width based on if its attacking a piece
                    if piece.isalpha():
                        # circle outline on piece
                        radius = self.piece_size // 2
                        width = self.line_size
                        colour = DARK_PINK
                    else:
                        # dot on square
                        radius = self.piece_size // 6
                        width = 0
                        colour = PINK

                    # create a surface and draw the circle on it
                    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, colour, (radius, radius), radius, width)

                    # draw the surface onto the screen
                    x = self.get_x(file + 0.5) - radius
                    y = self.get_y(rank + 0.5) - radius
                    screen.blit(surface, (x, y))

        # draw held piece
        if held_piece.pos:
            x, y = pygame.mouse.get_pos()
            screen.blit(self.images[held_piece.piece], (x - x_offset, y - y_offset))

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
