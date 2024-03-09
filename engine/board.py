from __future__ import annotations

from .move import Move

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Board:
    def __init__(self, board: str, white_move: bool) -> None:
        self.board = board
        self.white_move = white_move

    @classmethod
    def create(cls, fen: str = DEFAULT_FEN) -> Board:
        board = " " * 21
        for char in fen:
            if char.isdigit():
                board += "." * int(char)
            elif char == "/":
                board += " " * 2
            else:
                board += char
        board += " " * 21

        return cls(board, True)

    def make_move(self, move: Move) -> Board:
        board = list(self.board)
        board[move.dest] = board[move.pos]
        board[move.pos] = "."
        return Board("".join(board), not self.white_move)
