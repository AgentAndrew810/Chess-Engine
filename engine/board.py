from __future__ import annotations

from .move import Move
from .constants import DEFAULT_FEN, E, W



class Board:
    def __init__(self, board: str, white_move: bool, castle: list[bool]) -> None:
        self.board = board
        self.white_move = white_move
        self.castle = castle  # wk wq bk bq

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

        return cls(board, True, [True, True, True, True])

    def make_move(self, move: Move) -> Board:
        board = list(self.board)
        board[move.dest] = board[move.pos]
        board[move.pos] = "."

        if move.castling == "K":
            print("King Castling")
            board[move.pos + E] = board[move.dest + E]
            board[move.dest + E] = "."

        if move.castling == "Q":
            print("Queen Castling")
            board[move.pos + W] = board[move.dest + W * 2]
            board[move.dest + W * 2] = "."

        board = Board("".join(board), not self.white_move, self.castle)

        return board
