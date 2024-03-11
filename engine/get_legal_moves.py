from .board import Board
from .get_moves import get_moves
from .move import Move

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


def get_legal_moves(board: Board) -> list[Move]:
    moves = []

    for move in get_moves(board):
        child = board.make_move(move)

        # get the location of the king
        king = "K" if board.white_move else "k"
        king_loc = child.board.index(king)

        opp_moves = [move.dest for move in get_moves(child)]

        if king_loc in opp_moves:
            continue

        if move.castling:
            if move.dest == G1:
                if F1 in opp_moves:
                    continue
            if move.dest == C1:
                if D1 in opp_moves:
                    continue
            if move.dest == G8:
                if F8 in opp_moves:
                    continue
            if move.dest == C8:
                if D8 in opp_moves:
                    continue

            if move.pos in opp_moves:
                continue

        moves.append(move)
    return moves
