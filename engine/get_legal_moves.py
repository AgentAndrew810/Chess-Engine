from .board import Board
from .get_moves import get_moves
from .move import Move
from .constants import E, W


def get_legal_moves(board: Board) -> list[Move]:
    moves = []

    for move in get_moves(board):
        child = board.make_move(move)

        # get the location of the king
        king = "K" if board.white_move else "k"
        king_loc = child.board.index(king)

        opp_moves = [opp_move.dest for opp_move in get_moves(child)]

        if king_loc in opp_moves:
            continue

        if move.castling:
            if move.pos in opp_moves:
                continue

            if move.castling == "K":
                if move.dest + E in opp_moves:
                    continue

            if move.castling == "Q":
                if move.dest + W in opp_moves:
                    continue

        moves.append(move)
    return moves
