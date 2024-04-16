from __future__ import annotations
from random import getrandbits

from .move import Move
from .utils import get_pos
from .constants import DEFAULT_FEN, E, W, WKROOK, WQROOK, BKROOK, BQROOK, VALID_POS


class Board:
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

        # get en passant square
        if fen[3] != "-":
            self.ep = get_pos(fen[3])
        else:
            self.ep = 0

        # extra info for unmaking moves
        self.past_ep = []
        self.past_captures = []
        self.past_cr = []

        # zobrist keys
        self.zobrist_pieces = {}
        self.zobrist_ep = {}

        for pos in VALID_POS:
            # pieces
            self.zobrist_pieces[pos] = {}
            for piece in "pPkKnNbBrRqQ":
                self.zobrist_pieces[pos][piece] = getrandbits(64)
                
            # ep
            self.zobrist_ep[pos] = getrandbits(64)

        # side
        self.zobrist_side = getrandbits(64)

        # castling rights
        self.zobrist_cr = {"wk": getrandbits(64), "wq": getrandbits(64), "bk": getrandbits(64), "bq": getrandbits(64)}

    def get_zobrist(self) -> None:
        self.zobrist = 0

        for pos in VALID_POS:
            p = self.board[pos]
            if p not in " .":
                self.zobrist ^= self.zobrist_pieces[pos][p]

        if self.wck:
            self.zobrist ^= self.zobrist_cr["wk"]
        if self.wcq:
            self.zobrist ^= self.zobrist_cr["wq"]
        if self.bck:
            self.zobrist ^= self.zobrist_cr["bk"]
        if self.bcq:
            self.zobrist ^= self.zobrist_cr["bq"]
        
        if self.white_move:
            self.zobrist ^= self.zobrist_side
            
        if self.ep:
            self.zobrist ^= self.zobrist_ep[self.ep]

    def make(self, move: Move) -> None:
        piece = self.board[move.pos]
        target = self.board[move.dest]

        # make the move
        self.board[move.pos] = "."
        self.board[move.dest] = move.prom if move.prom else piece
        self.past_cr.append((self.wck, self.wcq, self.bck, self.bcq))
        self.past_ep.append(self.ep)
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
            self.board[move.ep] = "."

        # update en passant square (based on pawn double move)
        self.ep = (move.pos + move.dest) // 2 if move.double else 0

        # update castling rights and king_location if king moved
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
        
        self.get_zobrist()

    def unmake(self, move: Move) -> None:
        self.wck, self.wcq, self.bck, self.bcq = self.past_cr.pop()
        self.ep = self.past_ep.pop()
        new_piece = self.past_captures.pop()
        piece = self.board[move.dest]

        # update side to move
        self.white_move = not self.white_move

        # move the pieces back
        self.board[move.pos] = piece
        self.board[move.dest] = new_piece

        # undo promotion
        if move.prom:
            self.board[move.pos] = "P" if self.white_move else "p"

        # undo castling
        elif move.castling == "K":
            self.board[move.pos + E * 3] = self.board[move.pos + E]
            self.board[move.pos + E] = "."

        elif move.castling == "Q":
            self.board[move.pos + W * 4] = self.board[move.pos + W]
            self.board[move.pos + W] = "."

        # add piece taken by en passant back
        if move.ep:
            self.board[move.ep] = "p" if self.white_move else "P"
