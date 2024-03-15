from __future__ import annotations

from .move import Move
from .constants import DEFAULT_FEN, E, W, WKROOK, WQROOK, BKROOK, BQROOK


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
    def create(cls, full_fen: str = DEFAULT_FEN) -> Board:
        fen = full_fen.split(" ")

        # get the board
        board = " " * 21
        for char in fen[0]:
            if char.isdigit():
                board += "." * int(char)
            elif char == "/":
                board += " " * 2
            else:
                board += char
        board += " " * 21

        # get all additional stats
        white_move = fen[1] == "w"
        wcr = ("K" in fen[2], "Q" in fen[2])
        bcr = ("k" in fen[2], "q" in fen[2])

        return cls(board, white_move, wcr, bcr, -1)

    def make_move(self, move: Move) -> Board:
        board = list(self.board)
        piece = board[move.pos]

        # make the move
        board[move.pos] = "."
        board[move.dest] = move.prom if move.prom else piece

        # if castling move the rook
        if move.castling == "K":
            board[move.pos + E] = board[move.dest + E]
            board[move.dest + E] = "."

        elif move.castling == "Q":
            board[move.pos + W] = board[move.dest + W * 2]
            board[move.dest + W * 2] = "."

        # if en passant remove attacked piece
        if move.ep:
            board[self.ep] = "."

        # add en passant square
        ep = move.dest if move.double else -1

        # update castling rights if moved king or rook
        wck, wcq = self.wcr
        bck, bcq = self.bcr

        if piece == "K":
            wck, wcq = False, False

        elif piece == "k":
            bck, bcq = False, False

        elif piece == "R":
            if move.pos == WKROOK:
                wck = False
            elif move.pos == WQROOK:
                wcq = False

        elif piece == "r":
            if move.pos == BKROOK:
                bck = False
            elif move.pos == BQROOK:
                bcq = False

        # update castling rights if piece captured rook
        if move.dest == WKROOK:
            wck = False
        elif move.dest == WQROOK:
            wcq = False
        elif move.dest == BKROOK:
            bck = False
        elif move.dest == BQROOK:
            bcq = False

        return Board("".join(board), not self.white_move, (wck, wcq), (bck, bcq), ep)
