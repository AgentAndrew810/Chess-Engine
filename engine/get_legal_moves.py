from .board import Board
from .get_moves import get_moves
from .move import Move


def get_legal_moves(board: Board) -> list[Move]:
    moves = []

    for move in get_moves(board):
        child = board.make_move(move)

        # get the location of the king
        king = "K" if board.white_move else "k"
        king_loc = child.board.index(king)

        if king_loc not in [move.dest for move in get_moves(child)]:
            moves.append(move)

    return moves
