import pygame

from engine.board import Board
from gui.panel import Panel
from gui.drawnobject import DrawnObject
from gui.constants import BLACK, LIGHT, DARK


class Game(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.update()

        self.board = Board()
        self.panel = Panel()

        self.held_piece = ""
        self.held_piece_pos = None
        self.player_is_white = True
        self.white_pov = not self.player_is_white

    def update(self) -> None:
        # reload and resize image on window size changes
        self.load_images()

    def get_x(self, col: int | float) -> int:
        return round(self.x_padd + self.square_size * col)

    def get_y(self, row: int | float) -> int:
        return round(self.y_padd + self.square_size * row)

    def flip_rank_and_file(self, rank: int, file: int) -> tuple[int, int]:
        return (rank, file) if self.white_pov else (7 - rank, 7 - file)

    def grab_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return
        if not (self.y_padd < y < self.y_padd + self.board_size):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.square_size)
        file, self.x_offset = divmod(x - self.x_padd, self.square_size)

        # flip rank and file if playing as black
        rank, file = self.flip_rank_and_file(rank, file)
        piece = self.board.board[(rank + 2) * 10 + file + 1]

        # check if grabbing the correct colour
        if piece.isupper() == self.board.white_move:
            self.held_piece_pos = (rank, file)
            self.held_piece = piece

    def drop_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return
        if not (self.y_padd < y < self.y_padd + self.board_size):
            return

        self.held_piece = ""
        self.held_piece_pos = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(BLACK)
        self.panel.draw(screen)

        # draw each piece
        for pos in range(120):
            # get the piece, rank, and file
            piece = self.board.board[pos]
            rank = pos // 10 - 2
            file = pos % 10 - 1

            # flip the rank and file if black's pov
            rank, file = self.flip_rank_and_file(rank, file)

            if piece != " ":
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
            if piece.isalpha() and (rank, file) != self.held_piece_pos:
                screen.blit(
                    self.images[piece],
                    (
                        self.get_x(file) + self.line_size,
                        self.get_y(rank) + self.line_size,
                    ),
                )

        # draw held piece
        if self.held_piece.isalpha():
            x, y = pygame.mouse.get_pos()
            screen.blit(
                self.images[self.held_piece], (x - self.x_offset, y - self.y_offset)
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
