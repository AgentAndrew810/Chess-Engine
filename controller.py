import pygame

import gui
import engine


class GameController(gui.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        self.board_representation = engine.Board()
        self.board = gui.Board()
        self.panel = gui.Panel()

        self.held_piece = None
        self.player_is_white = True
        self.white_pov = not self.player_is_white
        self.x_offset = 0
        self.y_offset = 0

    def get_rank_file(self, pos: int) -> tuple[int, int]:
        rank, file = divmod(pos, 10)
        return rank - 2, file - 1

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
        piece = self.board_representation.board[(rank + 2) * 10 + file + 1]

        # check if grabbing the correct colour
        if piece.isupper() == self.board_representation.white_move:
            self.held_piece = (rank, file)

    def drop_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return
        if not (self.y_padd < y < self.y_padd + self.board_size):
            return

        self.held_piece = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(gui.BLACK)

        self.board.draw(
            screen,
            self.board_representation,
            self.white_pov,
            self.held_piece,
            self.x_offset,
            self.y_offset,
        )
        self.panel.draw(screen)
