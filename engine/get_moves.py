from .board import Board
from .move import Move
from .constants import OFFSETS, N, E, S, W, NE, NW, SE, SW


def get_moves(board: Board) -> list[Move]:
    moves = []

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

            # castling
            if piece == "K":
                if board.castle[0]:
                    if board.board[pos + E] == "." and board.board[pos + E * 2] == ".":
                        moves.append(Move(pos, pos + E * 2, False, "K"))

                if board.castle[1]:
                    if (
                        board.board[pos + W] == "."
                        and board.board[pos + W * 2] == "."
                        and board.board[pos + W * 3] == "."
                    ):
                        moves.append(Move(pos, pos + W * 2, False, "Q"))

            if piece == "k":
                if board.castle[2]:
                    if board.board[pos + E] == "." and board.board[pos + E * 2] == ".":
                        moves.append(Move(pos, pos + E * 2, False, "K"))

                if board.castle[3]:
                    if (
                        board.board[pos + W] == "."
                        and board.board[pos + W * 2] == "."
                        and board.board[pos + W * 3] == "."
                    ):
                        moves.append(Move(pos, pos + W * 2, False, "Q"))

    return moves
