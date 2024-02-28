from __future__ import annotations

from .constants import STARTING_BOARD


class Board:
    def __init__(self, board: str, white_move: bool) -> None:
        self.board = board
        self.white_move = white_move

    def starting_board(self) -> Board:
        board = STARTING_BOARD
        white_move = True

        return Board(board, white_move)
