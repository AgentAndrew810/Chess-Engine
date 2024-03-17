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

        if move.castling:
            dir = E if move.castling == "K" else W

            # add temp king's to where the king was and moves through in castling
            # this ensures pawns can still attack these squares in opp_moves
            temp_board = list(child.board)
            temp_board[move.pos], temp_board[move.pos + dir] = king, king
            child.board = "".join(temp_board)

        # get all the square the opponent can move
        opp_moves = [opp_move.dest for opp_move in get_moves(child)]

        # don't add move if opponent move to the king square (attack it)
        if king_loc in opp_moves:
            continue

        if move.castling:
            # don't add move if in check or moving through check
            if move.pos in opp_moves or move.pos + dir in opp_moves:
                continue

        moves.append(move)

    return moves
