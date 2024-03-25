from .board import Board
from .get_moves import get_moves
from .move import Move
from .constants import N, E, S, W


def get_legal_moves(board: Board) -> list[Move]:
    moves = []

    for move in get_moves(board):
        board.make(move)

        # get the location of the king
        king = "k" if board.white_move else "K"
        king_loc = board.board.index(king)

        # get all the square the opponent can move
        opp_moves = [opp_move.dest for opp_move in get_moves(board)]
        board.unmake(move)

        # don't add move if opponent move to the king square (attack it)
        if king_loc in opp_moves:
            continue

        if move.castling:
            opp_pawn = "p" if board.white_move else "P"
            up = N if board.white_move else S
            dir = E if move.castling == "K" else W

            # since pawn checks through castling don't register since there is no piece for the pawn to attack
            # this code manually adds the pawn moves by continuing if a pawn is in one of those 4 spots
            for side in (E, W):
                if board.board[move.pos + up + side] == opp_pawn:
                    opp_moves.append(move.pos)

                if board.board[move.pos + dir + up + side] == opp_pawn:
                    opp_moves.append(move.pos)

            # don't add move if in check or moving through check
            if move.pos in opp_moves or move.pos + dir in opp_moves:
                continue

        moves.append(move)

    return moves
