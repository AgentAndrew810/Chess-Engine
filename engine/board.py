from __future__ import annotations

from .move import Move
from .constants import DEFAULT_FEN, E, W


class Board:
    def __init__(
        self,
        board: str,
        white_move: bool,
        wcr: tuple[bool, bool],
        bcr: tuple[bool, bool],
        ep: int,
    ) -> None:
        self.board = board
        self.white_move = white_move
        self.wcr = wcr  # wk, wq
        self.bcr = bcr  # bk, bq
        self.ep = ep

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

        return cls(board, True, (True, True), (True, True), -1)

    def make_move(self, move: Move) -> Board:
        board = list(self.board)
        wck, wcq = self.wcr
        bck, bcq = self.bcr
        piece = board[move.pos]

        # make the move
        board[move.pos] = "."
        board[move.dest] = piece

        # if castling move the rook
        if move.castling == "K":
            board[move.pos + E] = board[move.dest + E]
            board[move.dest + E] = "."

        if move.castling == "Q":
            board[move.pos + W] = board[move.dest + W * 2]
            board[move.dest + W * 2] = "."

        # add en passant square
        ep = move.dest if move.double else -1

        # if promoting update the piece
        if move.prom:
            board[move.dest] = move.prom

        # if en passant remove attacked piece
        if move.ep:
            board[self.ep] = "."

        # update castling rights
        if piece == "K":
            wck, wcq = False, False

        if piece == "k":
            bck, bcq = False, False

        if piece == "R":
            if move.pos == 98:
                wck = False
            elif move.pos == 91:
                wcq = False

        if piece == "r":
            if move.pos == 28:
                bck = False
            elif move.pos == 21:
                bcq = False

        return Board("".join(board), not self.white_move, (wck, wcq), (bck, bcq), ep)
