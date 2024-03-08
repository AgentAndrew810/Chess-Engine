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
            for direction in OFFSETS[piece.upper()]:
                # get the new destination and piece
                dest = pos + direction
                new_piece = board.board[dest]

                # if sliding piece
                if piece.upper() in "BRQ":
                    while new_piece == "." or piece.isupper() != new_piece.isupper():
                        # break if off the board
                        if new_piece == " ":
                            break

                        if new_piece == ".":
                            # add the sliding move and keep going through loop
                            moves.append(Move(pos, dest, False))
                            dest += direction
                            new_piece = board.board[dest]
                        else:
                            # add the attacking move then break
                            moves.append(Move(pos, dest, True))
                            break
                else:
                    # don't do anything if off the board
                    if new_piece != " ":
                        # add the piece if blank square or opposing colour
                        if new_piece == "." or piece.isupper() != new_piece.isupper():
                            moves.append(Move(pos, dest, new_piece == "."))

    return moves
