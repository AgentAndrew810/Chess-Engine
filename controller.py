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

        self.player_is_white = True
        self.white_pov = True
        self.x_offset = 0
        self.y_offset = 0

    def grab_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return
        if not (self.y_padd < y < self.y_padd + self.board_size):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.square_size)
        file, self.x_offset = divmod(x - self.x_padd, self.square_size)

        # get the pos and piece
        pos = utils.get_pos(rank, file, self.white_pov)
        piece = self.board.board[pos]

        # check if grabbing the correct colour
        if piece.isupper() == self.board.white_move and piece.isalpha():
            self.held_piece.grab(rank, file, piece)

    def drop_piece(self, x: int, y: int) -> None:
        # check if the mouse is outside the board
        if not (self.x_padd < x < self.x_padd + self.board_size):
            pass
        if not (self.y_padd < y < self.y_padd + self.board_size):
            pass

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
