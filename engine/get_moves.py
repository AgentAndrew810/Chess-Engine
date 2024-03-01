from .board import Board
from .move import Move

# define directions
N, E, S, W = -10, 1, 10, -1

# define piece offsets
OFFSETS = {
    "N": (
        N * 2 + E,
        N * 2 + W,
        S * 2 + E,
        S * 2 + W,
        E * 2 + N,
        E * 2 + S,
        W * 2 + N,
        W * 2 + S,
    ),
    "B": (N + E, E + S, S + W, W + N),
    "R": (N, E, S, W),
    "Q": (N, N + E, E, E + S, S, S + W, W, W + N),
    "K": (N, N + E, E, E + S, S, S + W, W, W + N),
}


def get_legal_moves(board: Board) -> list[Move]:
    return []


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
                    moves.append(Move(pos, dest, False, False))
                elif new_piece.isupper() != piece.isupper():
                    moves.append(Move(pos, dest, True, False))

                if piece.upper() in "BRQ":
                    dest += dir
                    while new_piece == "." and new_piece.isupper() != piece.isupper():
                        if new_piece.isspace():
                            break

                        if new_piece == ".":
                            moves.append(Move(pos, dest, False, False))
                        else:
                            moves.append(Move(pos, dest, True, False))


    return moves
