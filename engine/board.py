from __future__ import annotations
from random import getrandbits

from .move import Move
from .utils import get_pos
from .constants import N, E, S, W, NE, NW, SE, SW
from .constants import DEFAULT_FEN, WKROOK, WQROOK, BKROOK, BQROOK, VALID_POS


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
        self.past_zobrist = []

        self.zobrist_init()

    def zobrist_init(self) -> None:
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

        self.hash = 0

        # self.hash = self.get_zobrist()

    def get_zobrist(self) -> None:
        self.hash = 0

        for pos in VALID_POS:
            p = self.board[pos]
            if p not in " .":
                self.hash ^= self.zobrist_pieces[pos][p]

        if self.wck:
            self.hash ^= self.zobrist_cr["wk"]
        if self.wcq:
            self.hash ^= self.zobrist_cr["wq"]
        if self.bck:
            self.hash ^= self.zobrist_cr["bk"]
        if self.bcq:
            self.hash ^= self.zobrist_cr["bq"]

        if self.white_move:
            self.hash ^= self.zobrist_side

        if self.ep:
            self.hash ^= self.zobrist_ep[self.ep]

    def make(self, move: Move) -> None:
        # get information
        piece = self.board[move.pos]
        target = self.board[move.dest]
        offset = move.dest - move.pos

        # store past information
        self.past_cr.append((self.wck, self.wcq, self.bck, self.bcq))
        self.past_ep.append(self.ep)
        self.past_captures.append(target)
        self.past_zobrist.append(self.hash)

        # make the move on the board
        self.board[move.pos] = "."
        self.board[move.dest] = piece

        # update hash
        self.hash ^= self.zobrist_pieces[move.pos][piece]  # remove piece on old square
        self.hash ^= self.zobrist_pieces[move.dest][piece]  # add piece to new square
        if target != ".":
            self.hash ^= self.zobrist_pieces[move.dest][target]  # remove captured piece

        if move.prom != "":
            # update hash
            self.hash ^= self.zobrist_pieces[move.dest][piece]  # remove the pawn
            self.hash ^= self.zobrist_pieces[move.dest][move.prom.upper() if self.white_move else move.prom]  # add the promotion piece

            self.board[move.dest] = move.prom.upper() if self.white_move else move.prom

        # if piece moved was a king
        if piece.upper() == "K":
            if offset == 2:  # king side castle
                rook = self.board[move.pos + E * 3]

                # update hash
                self.hash ^= self.zobrist_pieces[move.pos + E * 3][rook]  # remove rook
                self.hash ^= self.zobrist_pieces[move.pos + E][rook]  # add rook

                # move rook
                self.board[move.pos + E] = rook
                self.board[move.pos + E * 3] = "."

            elif offset == -2:  # queen side castle
                rook = self.board[move.pos + W * 4]

                # update hash
                self.hash ^= self.zobrist_pieces[move.pos + W * 4][rook]  # remove rook
                self.hash ^= self.zobrist_pieces[move.pos + W][rook]  # add rook

                # move rook
                self.board[move.pos + W] = rook
                self.board[move.pos + W * 4] = "."

            # update castling rights if king moved
            if piece == "K":
                self.wck, self.wcq = False, False
            else:
                self.bck, self.bcq = False, False

        # if made en passant move
        # based on if pawn made attack move without capturing a piece
        if piece.upper() == "P" and offset in (NE, NW, SE, SW) and target == ".":
            # update hash
            self.hash ^= self.zobrist_pieces[self.ep][self.board[self.ep]]  # remove pawn

            self.board[self.ep] = "."

        # if made pawn double move
        if piece.upper() == "P" and offset in (N * 2, S * 2):
            # update hash
            if self.ep != 0:
                self.hash ^= self.zobrist_ep[self.ep]  # if a non-zero en passant square, we have to remove the old one
            self.hash ^= self.zobrist_ep[move.dest]  # add hash of new ep square

            self.ep = move.dest

        else:
            # update hash
            if self.ep != 0:
                self.hash ^= self.zobrist_ep[self.ep]  # if a non-zero en passant square, we have to remove the old one

            self.ep = 0

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
        self.hash ^= self.zobrist_side

        #self.get_zobrist()

    def unmake(self, move: Move) -> None:
        self.wck, self.wcq, self.bck, self.bcq = self.past_cr.pop()
        self.ep = self.past_ep.pop()
        self.hash = self.past_zobrist.pop()

        target = self.past_captures.pop()
        piece = self.board[move.dest]
        offset = move.dest - move.pos

        # update side to move
        self.white_move = not self.white_move

        # move the pieces back
        self.board[move.pos] = piece
        self.board[move.dest] = target

        # undo promotion
        if move.prom:
            self.board[move.pos] = "P" if self.white_move else "p"

        # undo rook move if castling
        if piece.upper() == "K":
            if offset == 2:
                self.board[move.pos + E * 3] = self.board[move.pos + E]
                self.board[move.pos + E] = "."
            elif offset == -2:
                self.board[move.pos + W * 4] = self.board[move.pos + W]
                self.board[move.pos + W] = "."

        elif piece.upper() == "P":
            # if made attack move without capturing a piece -> en passant -> add back en passant piece
            if offset in (NE, NW, SE, SW) and target == ".":
                self.board[self.ep] = "p" if self.white_move else "P"
