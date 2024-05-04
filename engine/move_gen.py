from .board import Board
from .move import Move
from .constants import VALID_POS, N, E, S, W, OFFSETS, PROM_PIECES

# create tables of the moves each piece can make from each position
TARGETS = {}
for pos in VALID_POS:
    TARGETS[pos] = {}

    # white pawn
    TARGETS[pos]["P"] = [pos + N] if pos + N in VALID_POS else []
    if pos // 10 == 8:  # if on first rank
        TARGETS[pos]["P"] = [pos + N, pos + N * 2]
    TARGETS[pos]["Pa"] = {dir: pos + dir for dir in OFFSETS["Pa"] if pos + dir in VALID_POS}

    # black pawn
    TARGETS[pos]["p"] = [pos + S] if pos + S in VALID_POS else []
    if pos // 10 == 3:  # if on first rank
        TARGETS[pos]["p"] += [pos + S * 2] if pos + S * 2 in VALID_POS else []
    TARGETS[pos]["pa"] = {dir: pos + dir for dir in OFFSETS["pa"] if pos + dir in VALID_POS}

    # king and knight
    for p in "KN":
        TARGETS[pos][p] = [pos + dir for dir in OFFSETS[p] if pos + dir in VALID_POS]

    # bishop, rook, and queen moves
    for p in "BRQ":
        TARGETS[pos][p] = {}
        for dir in OFFSETS[p]:
            moves = []

            dest = pos + dir
            while dest in VALID_POS:
                moves.append(dest)
                dest += dir

            TARGETS[pos][p][dir] = moves


def move_gen(board: Board) -> list[Move]:
    king = "K" if board.white_move else "k"
    king_pos = board.board.index(king)

    pins, checks = get_pins_and_checks(board.board, board.white_move, king_pos)

    if len(checks) == 1:
        moves = get_all_moves(board, pins)

        check = checks[0]
        checking_piece_pos = check[0]
        checking_piece_dir = check[1]
        checking_piece = board.board[checking_piece_pos]

        valid_squares = []
        if checking_piece.upper() == "N":
            valid_squares = [checking_piece_pos]
        else:
            for dist in range(1, 8):
                valid_square = king_pos + checking_piece_dir * dist
                valid_squares.append(valid_square)
                if valid_square == checking_piece_pos:
                    break

        # filer out any move that isn't valid
        moves = [move for move in moves if move.pos == king_pos or move.dest in valid_squares]
        moves.extend(en_passant_moves(board, king_pos))
    elif len(checks) >= 2:
        moves = get_king_moves(board, king_pos)
    else:
        moves = get_all_moves(board, pins)
        moves.extend(en_passant_moves(board, king_pos))
        rook = "R" if board.white_move else "r"

        # add king-side castling moves
        if board.white_move and board.wck or not board.white_move and board.bck:
            if all(board.board[king_pos + E * i] == "." for i in range(1, 3)):
                if board.board[king_pos + E * 3] == rook:
                    checked1 = in_check(board.board, board.white_move, king_pos + E)
                    checked2 = in_check(board.board, board.white_move, king_pos + E * 2)
                    if not checked1 and not checked2:
                        moves.append(Move(king_pos, king_pos + E * 2))

        # add queen-side castling moves
        if board.white_move and board.wcq or not board.white_move and board.bcq:
            if all(board.board[king_pos + W * i] == "." for i in range(1, 4)):
                if board.board[king_pos + W * 4] == rook:
                    checked1 = in_check(board.board, board.white_move, king_pos + W)
                    checked2 = in_check(board.board, board.white_move, king_pos + W * 2)
                    if not checked1 and not checked2:
                        moves.append(Move(king_pos, king_pos + W * 2))

    return moves


def get_king_moves(board: Board, king_pos: int):
    moves = []
    king = board.board[king_pos]

    # remove the king (must do this so sliding piece will go through it)
    board.board[king_pos] = "."

    for dest in TARGETS[king_pos]["K"]:
        target = board.board[dest]

        # if friendly piece continue
        if target.isupper() == board.white_move and target != ".":
            continue

        # if the king is left in check continue
        if in_check(board.board, board.white_move, dest):
            continue

        if target == ".":
            moves.append(Move(king_pos, dest))
        else:
            moves.append(Move(king_pos, dest, capture=True))

    # add king back
    board.board[king_pos] = king
    return moves


def en_passant_moves(board: Board, king_pos: int):
    moves = []

    if board.ep:
        friendly_pawn = "P" if board.white_move else "p"
        pawn_forward_dir = N if board.white_move else S

        for side_dir in (E, W):
            friendly_pawn_loc = board.ep + side_dir
            target_square = board.ep + pawn_forward_dir

            if board.board[friendly_pawn_loc] == friendly_pawn:
                move = Move(friendly_pawn_loc, target_square)

                # check if it will leave king in check
                temp_board = board.board.copy()
                temp_board[move.dest] = temp_board[move.pos]
                temp_board[move.pos] = "."
                temp_board[board.ep] = "."
                checked = in_check(temp_board, board.white_move, king_pos)

                if not checked:
                    moves.append(move)
    return moves


def get_all_moves(board: Board, pins):
    moves = []
    last_rank = 2 if board.white_move else 9

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

        if p.upper() == "P":
            # pawn forward moves
            for dest in TARGETS[pos][p]:
                target = board.board[dest]

                if target == ".":
                    if not is_pinned or pin_dir in (N, S):
                        if dest // 10 == last_rank:
                            for prom in PROM_PIECES:
                                moves.append(Move(pos, dest, prom=prom))
                        else:
                            moves.append(Move(pos, dest))
                else:
                    break  # this is needed so that if there is a pawn double move it will be skipped (double pawn move can't jump over piece)
            # pawn attack moves
            for dir, dest in TARGETS[pos][p + "a"].items():
                target = board.board[dest]

                if target != "." and p.isupper() != target.isupper():
                    if not is_pinned or pin_dir in (dir, -dir):
                        if dest // 10 == last_rank:
                            for prom in PROM_PIECES:
                                moves.append(Move(pos, dest, prom=prom, capture=True))
                        else:
                            moves.append(Move(pos, dest, capture=True))

        elif p.upper() in "BRQ":
            # iterate through each direction, add the moves in that direction
            for dir, p_moves in TARGETS[pos][p.upper()].items():
                if is_pinned and pin_dir not in (dir, -dir):
                    continue

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

        elif p.upper() == "N":
            if not is_pinned:
                # loop through every possible move
                for dest in TARGETS[pos][p.upper()]:
                    target = board.board[dest]
                    # add the piece if blank square or opposing colour
                    if target == ".":
                        moves.append(Move(pos, dest))

                    elif p.isupper() != target.isupper():
                        moves.append(Move(pos, dest, capture=True))
        else:
            moves.extend(get_king_moves(board, pos))

    return moves


def in_check(board: list[str], white_move: bool, king_pos: int):
    for dir, positions in TARGETS[king_pos]["Q"].items():
        for dist, pos in enumerate(positions):
            # get the piece there
            piece = board[pos]
            ptype = piece.upper()

            if piece == ".":
                continue

            if piece.isupper() == white_move:
                # friendly piece -> no check from this direction
                break
            elif (
                # enemy piece giving check
                (ptype == "R" and dir in OFFSETS[ptype])  # rook and direction in rook directions
                or (ptype == "B" and dir in OFFSETS["B"])  # bishop and direction in bishop directions
                or (ptype == "Q")  # queen and any direction
                or (ptype == "K" and dist == 0)  # king and any direction, distance of 1
                or (ptype == "P" and dir in OFFSETS[piece + "ra"] and dist == 0)  # pawn and pawn attack direction, distance of 1
            ):
                # in check
                return True
            else:
                # enemy piece not giving check
                break

    # knight moves
    for pos in TARGETS[king_pos]["N"]:
        piece = board[pos]
        if piece.upper() == "N" and piece.isupper() != white_move:
            return True

    return False


def get_pins_and_checks(board: list[str], white_move: bool, king_pos: int):
    pins, checks = [], []

    for dir, positions in TARGETS[king_pos]["Q"].items():
        possible_pin = False

        for dist, pos in enumerate(positions):
            # get the piece there
            piece = board[pos]
            ptype = piece.upper()

            if piece == ".":
                continue

            # if friendly piece
            if piece.isupper() == white_move:
                # if the firsts piece, add it to posssible pin
                if not possible_pin:
                    possible_pin = (pos, dir)
                # otherwise break since there are two friendly pieces
                else:
                    break
            # enemy piece
            else:
                if (
                    (ptype == "R" and dir in OFFSETS[ptype])  # rook and direction in rook directions
                    or (ptype == "B" and dir in OFFSETS["B"])  # bishop and direction in bishop directions
                    or (ptype == "Q")  # queen and any direction
                    or (ptype == "K" and dist == 0)  # king and any direction, distance of 1
                    or (ptype == "P" and dir in OFFSETS[piece + "ra"] and dist == 0)  # pawn and pawn attack direction, distance of 1
                ):
                    # no piece is blocking -> in check
                    if not possible_pin:
                        checks.append((pos, dir))
                        break
                    # piece is blocking -> pinned piece
                    else:
                        pins.append(possible_pin)
                        break
                else:
                    # not giving check or pin
                    break

    for pos in TARGETS[king_pos]["N"]:
        piece = board[pos]

        if piece.upper() == "N" and piece.isupper() != white_move:
            checks.append((pos, dir))

    return pins, checks
