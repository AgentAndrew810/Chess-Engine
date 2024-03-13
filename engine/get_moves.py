from .board import Board
from .move import Move
from .constants import OFFSETS, N, E, S, W, NE, NW, SE, SW, PROM_PIECES


def get_moves(board: Board) -> list[Move]:
    moves = []

    # get info for pawns
    pawn_dir = N if board.white_move else S
    pawn_attack_moves = [NE, NW] if board.white_move else [SE, SW]
    first_rank, last_rank = (8, 2) if board.white_move else (3, 9)

    # for pos, p in enumerate(board.board):
    for pos in range(21, 99):
        p = board.board[pos]

        # skip blank squares and wrong colour
        if p in " ." or p.isupper() != board.white_move:
            continue

        if p.upper() == "P":
            # add en passant moves
            for side_dir in [E, W]:
                if pos + side_dir == board.ep:
                    moves.append(Move(pos, pos + pawn_dir + side_dir, ep=True))

            # add normal pawn moves
            dest = pos + pawn_dir
            if board.board[dest] == ".":
                if dest // 10 == last_rank:
                    # promotion
                    for prom in PROM_PIECES:
                        prom = prom.upper() if board.white_move else prom
                        moves.append(Move(pos, dest, prom=prom))

                else:
                    moves.append(Move(pos, dest))

                # if on first rank, add the double pawn move
                if pos // 10 == first_rank:
                    dest += pawn_dir
                    if board.board[dest] == ".":
                        moves.append(Move(pos, dest, double=True))

            # add pawn attacking moves
            for dir in pawn_attack_moves:
                dest = pos + dir
                target = board.board[dest]

                if target not in " ." and p.isupper() != target.isupper():
                    if dest // 10 == last_rank:
                        for prom in PROM_PIECES:
                            prom = prom.upper() if board.white_move else prom
                            moves.append(Move(pos, dest, prom=prom))

                    else:
                        moves.append(Move(pos, dest, capture=True))

        else:
            for dir in OFFSETS[p.upper()]:
                dest = pos + dir
                target = board.board[dest]

                # if sliding p
                if p.upper() in "BRQ":
                    while target == "." or p.isupper() != target.isupper():
                        # break if off the board
                        if target == " ":
                            break

                        # break if hit p, otherwise keep going
                        if target == ".":
                            moves.append(Move(pos, dest))
                            dest += dir
                            target = board.board[dest]
                        else:
                            moves.append(Move(pos, dest, capture=True))
                            break
                else:
                    if target != " ":
                        # add the p if blank square or opposing colour
                        if target == "." or p.isupper() != target.isupper():
                            moves.append(Move(pos, dest, capture=target != "."))

            # castling
            if p == "K" and board.wcr[0] or p == "k" and board.bcr[0]:
                if board.board[pos + E] == "." and board.board[pos + E * 2] == ".":
                    moves.append(Move(pos, pos + E * 2, castling="K"))

            if p == "K" and board.wcr[1] or p == "k" and board.bcr[1]:
                if (
                    board.board[pos + W] == "."
                    and board.board[pos + W * 2] == "."
                    and board.board[pos + W * 3] == "."
                ):
                    moves.append(Move(pos, pos + W * 2, castling="Q"))

    return moves
