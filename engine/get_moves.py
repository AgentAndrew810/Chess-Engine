from .board import Board
from .move import Move
from .constants import (
    POS_ON_BOARD,
    N,
    E,
    S,
    W,
    NE,
    NW,
    SE,
    SW,
    PROM_PIECES,
    VALID_MOVES,
)


def get_moves(board: Board) -> list[Move]:
    moves = []

    # get info for pawns
    if board.white_move:
        pawn_dir = N
        pawn_attack_moves = [NE, NW]
        first_rank, last_rank = 8, 2
    else:
        pawn_dir = S
        pawn_attack_moves = [SE, SW]
        first_rank, last_rank = 3, 9
        
    rook = "R" if board.white_move else "r"
    

    for pos in POS_ON_BOARD:
        p = board.board[pos]

        # skip blank squares and wrong colour
        if p == "." or p.isupper() != board.white_move:
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
            if p.upper() in "BRQ":
                # iterate through each direction, and the moves in that direction
                for dir, p_moves in VALID_MOVES[pos][p.upper()].items():
                    # loop through every position in those moves
                    for dest in p_moves:
                        target = board.board[dest]

                        # if no piece add the move
                        if target == ".":
                            moves.append(Move(pos, dest))
                        else:
                            # if enemy piece add the move
                            if p.isupper() != target.isupper():
                                moves.append(Move(pos, dest, capture=True))
                            # if friendly or enemy exit the p_moves loop (exiting all moves in this direction)
                            break

            else:
                # loop through every possible move
                for dest in VALID_MOVES[pos][p.upper()]:
                    target = board.board[dest]
                    # add the piece if blank square or opposing colour
                    if target == ".":
                        moves.append(Move(pos, dest))

                    elif p.isupper() != target.isupper():
                        moves.append(Move(pos, dest, capture=True))


                # Check for king-side castling
                if p == "K" and board.wck or p == "k" and board.bck:
                    if all(board.board[pos + E * i] == "." for i in range(1, 3)):
                        if board.board[pos + E * 3] == rook:
                            moves.append(Move(pos, pos + E * 2, castling="K"))

                # Check for queen-side castling
                if p == "K" and board.wcq or p == "k" and board.bcq:
                    if all(board.board[pos + W * i] == "." for i in range(1, 4)):
                        if board.board[pos + W * 4] == rook:
                            moves.append(Move(pos, pos + W * 2, castling="Q"))

    return moves
