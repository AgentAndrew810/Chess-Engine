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

        # don't add move if opponent can attack king
        if king_loc in opp_moves:
            continue

        if move.castling:
            dir = E if move.castling == "K" else W

            # don't add move if in check or moving through check
            if move.pos or move.dest + dir in opp_moves:
                continue
        moves.append(move)
        
    return moves
