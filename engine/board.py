from __future__ import annotations

from .move import Move
from .constants import DEFAULT_FEN, E, W, WKROOK, WQROOK, BKROOK, BQROOK


class Board:
    __slots__ = (
        "board",
        "white_move",
        "wck",
        "wcq",
        "bck",
        "bcq",
        "ep",
        "past_moves",
        "past_captures",
        "past_cr",
    )

    def __init__(self, full_fen: str = DEFAULT_FEN) -> None:
        fen = full_fen.split(" ")
        # get the board
        self.board = [" "] * 21
        for char in fen[0]:
            if char.isdigit():
                self.board.extend(["."] * int(char))
            elif char == "/":
                self.board.extend([" "] * 2)
            else:
                self.board.append(char)
        self.board.extend([" "] * 21)

        # get all additional stats
        self.white_move = fen[1] == "w"
        self.wck, self.wcq = ["K" in fen[2], "Q" in fen[2]]
        self.bck, self.bcq = ["k" in fen[2], "q" in fen[2]]
        self.ep = 0

        # extra info for unmaking moves
        self.past_moves = [Move(-1, -1)]  # set for drawing past move on board
        self.past_captures = []
        self.past_cr = []

    def make(self, move: Move) -> None:
        piece = self.board[move.pos]
        target = self.board[move.dest]

        # make the move
        self.board[move.pos] = "."
        self.board[move.dest] = move.prom if move.prom else piece
        self.past_cr.append((self.wck, self.wcq, self.bck, self.bcq))
        self.past_moves.append(move)
        self.past_captures.append(target)

        # if castling move the rook
        if move.castling == "K":
            self.board[move.pos + E] = self.board[move.pos + E * 3]
            self.board[move.pos + E * 3] = "."

        elif move.castling == "Q":
            self.board[move.pos + W] = self.board[move.pos + W * 4]
            self.board[move.pos + W * 4] = "."

        # if en passant remove attacked piece
        if move.ep:
            self.board[self.ep] = "."

        # update en passant square (based on pawn double move)
        self.ep = move.dest if move.double else 0

        # update castling rights if moved king or rook
        if piece == "K":
            self.wck, self.wcq = False, False
        elif piece == "k":
            self.bck, self.bcq = False, False

        # check if move.pos is where rooks should be (no need to check if they are rooks)
        # since if it isn't the rooks castling rights will be gone anyways
        if move.pos == WKROOK:
            self.wck = False
        elif move.pos == WQROOK:
            self.wcq = False
        elif move.pos == BKROOK:
            self.bck = False
        elif move.pos == BQROOK:
            self.bcq = False

        # update side to move
        self.white_move = not self.white_move

    def unmake(self) -> None:
        self.wck, self.wcq, self.bck, self.bcq = self.past_cr.pop()
        new_piece = self.past_captures.pop()
        undo_move = self.past_moves.pop()
        prior_move = self.past_moves[-1]

        # update side to move
        self.white_move = not self.white_move

        # move the pieces back
        self.board[undo_move.pos] = self.board[undo_move.dest]
        self.board[undo_move.dest] = new_piece

        # undo promotion
        if undo_move.prom:
            self.board[undo_move.pos] = "P" if self.white_move else "p"

        # undo castling
        elif undo_move.castling == "K":
            self.board[undo_move.pos + E * 3] = self.board[undo_move.pos + E]
            self.board[undo_move.pos + E] = "."

        elif undo_move.castling == "Q":
            self.board[undo_move.pos + W * 4] = self.board[undo_move.pos + W]
            self.board[undo_move.pos + W] = "."

        # add ep square back
        if prior_move.double:
            self.ep = prior_move.dest
        else:
            self.ep = 0

        # add piece taken by en passant back
        if undo_move.ep:
            self.board[self.ep] = "p" if self.white_move else "P"
