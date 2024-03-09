import pygame

import game
import engine
import utils


class GameController(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        self.board = engine.Board()
        self.board_gui = game.Board()
        self.panel = game.Panel()
        self.held_piece = game.HeldPiece()
        self.next_moves = engine.get_moves(self.board)

        self.player_is_white = True
        self.white_pov = self.player_is_white
        self.x_offset = 0
        self.y_offset = 0

    def outside_board(self, x: int, y: int) -> bool:
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return True
        elif not (self.y_padd < y < self.y_padd + self.board_size):
            return True

        return False

    def grab_piece(self, x: int, y: int) -> None:
        if self.outside_board(x, y):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.square_size)
        file, self.x_offset = divmod(x - self.x_padd, self.square_size)

        # get the pos and piece
        pos = utils.get_pos(rank, file, self.white_pov)
        piece = self.board.board[pos]

        # check if grabbing the correct colour
        if piece.isupper() == self.board.white_move and piece.isalpha():
            self.held_piece.grab(pos, piece, self.next_moves)

    def drop_piece(self, x: int, y: int) -> None:
        if self.outside_board(x, y):
            return

        self.held_piece.drop()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(game.BLACK)

        self.board_gui.draw(
            screen,
            self.board,
            self.white_pov,
            self.held_piece,
            self.x_offset,
            self.y_offset,
        )
        self.panel.draw(screen)
