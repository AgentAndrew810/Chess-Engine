from .board import Board
from .move import Move
from .constants import OFFSETS


def get_moves(board: Board) -> list[Move]:
    moves = []

    for pos, piece in enumerate(board.board):
        # skip blank squares and wrong colour
        if piece in " ." or piece.isupper() != board.white_move:
            continue

        if piece.upper() == "P":
            pass

        else:
            for dir in OFFSETS[piece.upper()]:
                dest = pos + dir
                new_piece = board.board[dest]

                # skip off board
                if new_piece.isspace():
                    continue

                if new_piece == ".":
                    moves.append(Move(pos, dest, False))

                elif new_piece.isupper() != piece.isupper():
                    moves.append(Move(pos, dest, True))

                if piece.upper() in "BRQ":
                    dest += dir
                    while new_piece == "." or new_piece.isupper() != piece.isupper():
                        if new_piece.isspace():
                            break

                        if new_piece == ".":
                            moves.append(Move(pos, dest, False))
                        else:
                            moves.append(Move(pos, dest, True))

    return moves
