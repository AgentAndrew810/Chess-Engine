from __future__ import annotations

from .move import Move

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

# positions for castling
A1 = 91
B1 = 92
C1 = 93
D1 = 94
E1 = 95
F1 = 96
G1 = 97
H1 = 98

A8 = 21
B8 = 22
C8 = 23
D8 = 24
E8 = 25
F8 = 26
G8 = 27
H8 = 28


class Board:
    def __init__(self, board: str, starter_options: bool) -> None:
        self.board = board

        if starter_options:
            self.white_move = True
            self.wk, self.wq, self.bk, self.bq = True, True, True, True

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

        if move.castling:
            if move.dest == G1:
                board[F1] = "R"
                board[H1] = "."
            if move.dest == C1:
                board[D1] = "R"
                board[A1] = "."
            if move.dest == G8:
                board[F8] = "r"
                board[H8] = "."
            if move.dest == C8:
                board[D8] = "r"
                board[A8] = "."

        board = Board("".join(board), False)
        board.wk, board.wq, board.bk, board.bq = self.wk, self.wq, self.bk, self.bq
        board.white_move = not self.white_move

        return board
