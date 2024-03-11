from .board import Board
from .move import Move

# define directions
N, E, S, W = -10, 1, 10, -1
NE, NW, SE, SW = -9, -11, 11, 9

# define piece offsets
OFFSETS = {
    "N": (N + NE, N + NW, S + SE, S + SW, E + NE, E + SE, W + NW, W + SW),
    "B": (NE, NW, SE, SW),
    "R": (N, E, S, W),
    "Q": (N, NE, E, SE, S, SW, W, NW),
    "K": (N, NE, E, SE, S, SW, W, NW),
}

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


def get_moves(board: Board) -> list[Move]:
    moves = []

    # castling moves
    if board.wk:
        if board.board[F1] == "." and board.board[G1] == "." and board.board[H1] == "R":
            moves.append(Move(E1, G1, False, True))

    if board.wq:
        if (
            board.board[D1] == "."
            and board.board[C1] == "."
            and board.board[B1] == "."
            and board.board[A1] == "R"
        ):
            moves.append(Move(E1, C1, False, True))

    if board.bk:
        if board.board[F8] == "." and board.board[G8] == "." and board.board[H8] == "r":
            moves.append(Move(E8, G8, False, True))

    if board.bq:
        if (
            board.board[D8] == "."
            and board.board[C8] == "."
            and board.board[B8] == "."
            and board.board[A8] == "r"
        ):
            moves.append(Move(E8, C8, False, True))

    for pos, piece in enumerate(board.board):
        # skip blank squares and wrong colour
        if piece in " ." or piece.isupper() != board.white_move:
            continue

        if piece.upper() == "P":
            # get the destination and piece
            dir, first_rank = (N, 8) if piece.isupper() else (S, 3)
            dest = pos + dir

            # add the normal pawn move
            if board.board[dest] == ".":
                moves.append(Move(pos, dest, False))

                # if on first rank
                if pos // 10 == first_rank:
                    dest += dir
                    # add the double pawn move
                    if board.board[dest] == ".":
                        moves.append(Move(pos, dest, False))

            # add attacking moves
            for dir in (NE, NW) if piece.isupper() else (SE, SW):
                dest = pos + dir
                new_piece = board.board[dest]

                if new_piece.isalpha() and piece.isupper() != new_piece.isupper():
                    moves.append(Move(pos, dest, True))

        else:
            for dir in OFFSETS[piece.upper()]:
                # get the new destination and piece
                dest = pos + dir
                new_piece = board.board[dest]

                # if sliding piece
                if piece.upper() in "BRQ":
                    while new_piece == "." or piece.isupper() != new_piece.isupper():
                        # break if off the board
                        if new_piece == " ":
                            break

                        # break if hit piece, otherwise keep going
                        if new_piece == ".":
                            moves.append(Move(pos, dest, False))
                            dest += dir
                            new_piece = board.board[dest]
                        else:
                            moves.append(Move(pos, dest, True))
                            break
                else:
                    if new_piece != " ":
                        # add the piece if blank square or opposing colour
                        if new_piece == "." or piece.isupper() != new_piece.isupper():
                            moves.append(Move(pos, dest, new_piece != "."))

    return moves
