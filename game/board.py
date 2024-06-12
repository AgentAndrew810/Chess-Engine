import pygame

import engine
from .utils import get_pos
from .heldpiece import HeldPiece
from .drawnobject import DrawnObject
from .constants import LIGHT, DARK, HELD_COLOUR, ATTACK_COLOUR, TARGET_COLOUR, PAST_MOVE_COLOUR


class Board(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

    def update(self) -> None:
        # determine variables
        self.line_size = round(self.unit / 20)
        self.piece_size = self.unit - self.line_size * 2

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

        # resize each image to piece size
        for name, image in self.images.items():
            self.images[name] = pygame.transform.smoothscale(image, (self.piece_size, self.piece_size))

    def get_x(self, col: int | float) -> int:
        return round(self.x_padd + self.unit * col)

    def get_y(self, row: int | float) -> int:
        return round(self.y_padd + self.unit * row)

    def highlight_square(self, screen: pygame.surface.Surface, rank: int, file: int, colour: tuple[int, int, int, int]) -> None:
        rect = pygame.Rect(self.get_x(file), self.get_y(rank), self.unit, self.unit)
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.fill(colour)
        screen.blit(s, rect)

    def draw(
        self,
        screen: pygame.surface.Surface,
        board: engine.Board,
        white_pov: bool,
        held_piece: HeldPiece,
        last_move: engine.Move,
        highlight_last_move: bool,
        x_offset: int,
        y_offset: int,
    ) -> None:
        for rank in range(8):
            for file in range(8):
                # get the pos and piece
                pos = get_pos(rank, file, white_pov)
                piece = board.board[pos]

                # draw background square
                if piece not in " ":
                    colour = LIGHT if (rank + file) % 2 == 0 else DARK

                    pygame.draw.rect(
                        screen,
                        colour,
                        (self.get_x(file), self.get_y(rank), self.unit, self.unit),
                    )

                # highlight last move
                if highlight_last_move:
                    if pos in (last_move.pos, last_move.dest):
                        self.highlight_square(screen, rank, file, PAST_MOVE_COLOUR)

                # highlight held piece
                if pos == held_piece.pos:
                    self.highlight_square(screen, rank, file, HELD_COLOUR)

                # draw the piece
                if piece not in " .":
                    # if the position is not the held piece or the piece is not held (just selected)
                    if pos != held_piece.pos or not held_piece.held:
                        screen.blit(
                            self.images[piece],
                            (self.get_x(file) + self.line_size, self.get_y(rank) + self.line_size),
                        )

                if pos in held_piece.moves:
                    # determine the radius and width based on if its attacking a piece
                    if piece.isalpha():
                        # circle outline on piece
                        radius = self.piece_size // 2
                        width = self.line_size
                        colour = ATTACK_COLOUR
                    else:
                        # dot on square
                        radius = self.piece_size // 5.5
                        width = 0
                        colour = TARGET_COLOUR

                    # create a surface and draw the circle on it
                    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, colour, (radius, radius), radius, width)

                    # draw the surface onto the screen
                    x = self.get_x(file + 0.5) - radius
                    y = self.get_y(rank + 0.5) - radius
                    screen.blit(surface, (x, y))

        # draw held piece
        if held_piece.pos and held_piece.held:
            x, y = pygame.mouse.get_pos()
            screen.blit(self.images[held_piece.piece], (x - x_offset, y - y_offset))

        # draw board border
        pygame.draw.rect(screen, (0, 0, 0), (self.x_padd, self.y_padd, self.unit * 8, self.unit * 8), self.line_size)
