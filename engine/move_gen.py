from .board import Board
from .move import Move

DIRECTIONS = [-10, -1, 1, 10, -11, -9, 9, 11]
VALID_POS = [num for start in range(21, 92, 10) for num in range(start, start + 8)]
KNIGHT_MOVES = [-19, -21, 21, 19, -8, 12, -12, 8]

N, E, S, W = -10, 1, 10, -1
NE, NW, SE, SW = -9, -11, 11, 9

OFFSETS = {
    "p": [S, SE, SW],
    "P": [N, NE, NW],
    "N": [N + NE, N + NW, S + SE, S + SW, E + NE, E + SE, W + NW, W + SW],
    "B": [NE, NW, SE, SW],
    "R": [N, E, S, W],
    "Q": [N, NE, E, SE, S, SW, W, NW],
    "K": [N, NE, E, SE, S, SW, W, NW],
}

PROM_PIECES = ["b", "n", "r", "q"]

# create tables of the moves each piece can make from each position
MOVE_TABLES = {}
for pos in VALID_POS:
    MOVE_TABLES[pos] = {}

    # pawn moves
    MOVE_TABLES[pos]["p"] = {dir: pos + dir for dir in OFFSETS["p"] if pos+dir in VALID_POS}
    MOVE_TABLES[pos]["P"] = {dir: pos + dir for dir in OFFSETS["P"] if pos+dir in VALID_POS}

    # king and knight moves
    for p in "KN":
        MOVE_TABLES[pos][p] = [
            pos + dir for dir in OFFSETS[p] if pos + dir in VALID_POS
        ]

    # bishop, rook, and queen moves
    for p in "BRQ":
        MOVE_TABLES[pos][p] = {}
        for dir in OFFSETS[p]:
            moves = []

            dest = pos + dir
            while dest in VALID_POS:
                moves.append(dest)
                dest += dir

            MOVE_TABLES[pos][p][dir] = moves


def move_gen(board: Board):
    king = "K" if board.white_move else "k"
    king_pos = board.board.index(king)

    in_check, pins, checks = get_pins_and_checks(board, king_pos)

    if in_check:
        if len(checks) == 1:
            moves = get_all_moves(board, pins)
            check = checks[0]
            checking_piece_pos = check[0]
            checking_piece_dir = check[1]
            piece_checking = board.board[checking_piece_pos]
            valid_squares = []
            if piece_checking.upper() == "N":
                valid_squares = [checking_piece_pos]
            else:
                for dist in range(1, 8):
                    valid_square = king_pos + checking_piece_dir * dist
                    valid_squares.append(valid_square)
                    if valid_square == checking_piece_pos:
                        break
            moves = list(
                filter(lambda x: x.pos == king_pos or x.dest in valid_squares, moves)
            )
        else:
            moves = get_king_moves(board, pos)
    else:
        moves = get_all_moves(board, pins)

    return moves


def get_king_moves(board: Board, pos: int):
    moves = []
    p = board.board[pos]
    for dest in MOVE_TABLES[pos]["K"]:
        in_check, _, _ = get_pins_and_checks(board, dest)
        target = board.board[dest]

        if in_check:
            continue

        # add the piece if blank square or opposing colour
        if target == ".":
            moves.append(Move(pos, dest))
        elif p.isupper() != target.isupper():
            moves.append(Move(pos, dest, capture=True))

    return moves


def get_all_moves(board: Board, pins):
    moves = []

    first_rank, last_rank = (8, 2) if board.white_move else (3, 9)

    for pos in VALID_POS:
        p = board.board[pos]

        # skip blank squares and wrong colour
        if p == "." or p.isupper() != board.white_move:
            continue

        is_pinned = False
        for pin in pins:
            if pin[0] == pos:
                is_pinned = True
                pin_dir = pin[1]
                pins.remove(pin)
                break

        if p.upper() == "P":
            #     # add en passant moves
            #     for side_dir in [E, W]:
            #         if pos + side_dir == board.ep:
            #             moves.append(Move(pos, pos + pawn_dir + side_dir, ep=True))

            for dir, dest in MOVE_TABLES[pos][p].items():
                target = board.board[dest]

                if target == "." and abs(dir) == 10:
                    if not is_pinned or pin_dir in (dir, -dir):
                        if dest // 10 == last_rank:
                            for prom in PROM_PIECES:
                                prom = prom.upper() if board.white_move else prom
                                moves.append(Move(pos, dest, prom=prom))
                        else:
                            moves.append(Move(pos, dest))

                            # pawn double move
                            if pos // 10 == first_rank:
                                dest += dir
                                target = board.board[dest]
                                if target == ".":
                                    moves.append(Move(pos, dest, double=True))
                elif (
                    target != "."
                    and p.isupper() != target.isupper()
                    and abs(dir) in (9, 11)
                ):
                    if not is_pinned or pin_dir in (dir, -dir):
                        if dest // 10 == last_rank:
                            for prom in PROM_PIECES:
                                prom = prom.upper() if board.white_move else prom
                                moves.append(Move(pos, dest, prom=prom))
                        else:
                            moves.append(Move(pos, dest, capture=True))

        elif p.upper() in "BRQ":
            # iterate through each direction, and the moves in that direction
            for dir, p_moves in MOVE_TABLES[pos][p.upper()].items():
                # loop through every position in those moves
                for dest in p_moves:
                    target = board.board[dest]

                    # if no piece add the move
                    if target == ".":
                        if not is_pinned or pin_dir in (dir, -dir):
                            moves.append(Move(pos, dest))
                    else:
                        # if enemy piece add the move
                        if p.isupper() != target.isupper():
                            if not is_pinned or pin_dir in (dir, -dir):
                                moves.append(Move(pos, dest, capture=True))
                        # if friendly or enemy exit the p_moves loop (exiting all moves in this direction)
                        break

        elif p.upper() == "N":
            # loop through every possible move
            for dest in MOVE_TABLES[pos][p.upper()]:
                target = board.board[dest]
                # add the piece if blank square or opposing colour
                if target == ".":
                    if not is_pinned:
                        moves.append(Move(pos, dest))

                elif p.isupper() != target.isupper():
                    if not is_pinned:
                        moves.append(Move(pos, dest, capture=True))

        else:
            moves.extend(get_king_moves(board, pos))

    return moves


def get_pins_and_checks(board: Board, king_pos: int):
    pins, checks = [], []
    in_check = False

    for i in range(8):
        dir = DIRECTIONS[i]
        possible_pin = False
        for dist in range(1, 8):
            # get the piece and destination
            dest = king_pos + dir * dist
            piece = board.board[dest]
            is_white = piece.isupper()

            if piece == ".":
                continue

            if piece != " ":
                # if friendly piece
                if is_white == board.white_move and piece.upper() != "K":
                    # if the first piece, add it to possible pin
                    if not possible_pin:
                        possible_pin = (dest, dir)
                    # otherwise break since there are two friendly pieces
                    else:
                        break
                # enemy piece
                elif is_white != board.white_move:
                    if (
                        (0 <= i <= 3 and piece.upper() == "R")
                        or (4 <= i <= 7 and piece.upper() == "B")
                        or (0 <= i <= 7 and piece.upper() == "Q")
                        or (
                            dist == 1
                            and piece.upper() == "P"
                            and (
                                (is_white and 6 <= i <= 7)
                                or (not is_white and 4 <= i <= 5)
                            )
                        )
                        or (dist == 1 and piece.upper() == "K")
                    ):
                        # no piece is blocking -> in check
                        if not possible_pin:
                            in_check = True
                            checks.append((dest, dir))
                            break
                        # piece is blocking -> pinned piece
                        else:
                            pins.append(possible_pin)
                            break
                    else:
                        # not giving check or pin
                        break
            else:
                # off board
                break

    for dir in KNIGHT_MOVES:
        dest = king_pos + dir
        piece = board.board[dest]
        if dest in VALID_POS:
            if piece.upper() == "N" and piece.isupper() != board.white_move:
                in_check = True
                checks.append((dest, dir))

    return in_check, pins, checks
