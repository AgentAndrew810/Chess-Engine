from .board import Board
from .move import Move
from .constants import VALID_POS, N, E, S, W, OFFSETS
from .precalculated_data import MOVE_TABLES, LINE_OF_SIGHT, LINE_OF_SIGHT_KNIGHT


def move_gen(board: Board, captures_only: bool = False) -> list[Move]:
    king_pos = board.wk_pos if board.white_move else board.bk_pos
    pins, checks = get_pins_and_checks(board, king_pos)

    if len(checks) == 0:
        if captures_only:
            moves = get_all_captures(board, pins)
        else:
            moves = get_all_moves(board, pins)
            rook = "R" if board.white_move else "r"

            # add king-side castling moves
            if board.white_move and board.wck or not board.white_move and board.bck:
                if all(board.board[king_pos + E * i] == "." for i in range(1, 3)):
                    if board.board[king_pos + E * 3] == rook:
                        checked1 = in_check(board, king_pos + E)
                        checked2 = in_check(board, king_pos + E * 2)
                        if not checked1 and not checked2:
                            moves.append(Move(king_pos, king_pos + E * 2))

            # add queen-side castling moves
            if board.white_move and board.wcq or not board.white_move and board.bcq:
                if all(board.board[king_pos + W * i] == "." for i in range(1, 4)):
                    if board.board[king_pos + W * 4] == rook:
                        checked1 = in_check(board, king_pos + W)
                        checked2 = in_check(board, king_pos + W * 2)
                        if not checked1 and not checked2:
                            moves.append(Move(king_pos, king_pos + W * 2))
    elif len(checks) == 1:
        if captures_only:
            moves = get_all_captures(board, pins)
        else:
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
        moves = [move for move in moves if move.dest in valid_squares]

    else:
        moves = []

    if captures_only:
        moves.extend(get_king_captures(board, king_pos))
    else:
        moves.extend(get_king_moves(board, king_pos))

    moves.extend(en_passant_moves(board, king_pos))

    return moves


def get_king_moves(board: Board, king_pos: int):
    moves = []
    king = board.board[king_pos]

    # remove the king (must do this so sliding piece will go through it)
    board.board[king_pos] = "."

    for move in MOVE_TABLES[king_pos]["K"]:
        target = board.board[move.dest]

        # if ally piece continue
        if target in board.ally_pieces:
            continue

        # if the king is left in check continue
        if in_check(board, move.dest):
            continue

        moves.append(move)

    # add king back
    board.board[king_pos] = king
    return moves


def get_king_captures(board: Board, king_pos: int):
    moves = []
    king = board.board[king_pos]

    # remove the king (must do this so sliding piece will go through it)
    board.board[king_pos] = "."

    for move in MOVE_TABLES[king_pos]["K"]:
        target = board.board[move.dest]

        # if blank square or ally piece continue
        if target == "." or target in board.ally_pieces:
            continue

        # if the king is left in check continue
        if in_check(board, move.dest):
            continue

        moves.append(move)

    # add king back
    board.board[king_pos] = king
    return moves


def en_passant_moves(board: Board, king_pos: int):
    moves = []

    if board.ep != 0:
        friendly_pawn = "P" if board.white_move else "p"
        enemy_pawn = "p" if board.white_move else "P"
        pawn_forward_dir = N if board.white_move else S

        for side_dir in (E, W):
            friendly_pawn_loc = board.ep + side_dir
            target_square = board.ep + pawn_forward_dir

            if board.board[friendly_pawn_loc] == friendly_pawn:
                move = Move(friendly_pawn_loc, target_square)

                # make the move on the board
                board.board[board.ep] = "."
                board.board[friendly_pawn_loc] = "."
                board.board[target_square] = friendly_pawn

                # determine if move will leave king in check
                checked = in_check(board, king_pos)

                # undo the move
                board.board[board.ep] = enemy_pawn
                board.board[friendly_pawn_loc] = friendly_pawn
                board.board[target_square] = "."

                if not checked:
                    moves.append(move)
    return moves


def get_all_moves(board: Board, pins):
    moves = []

    for pos in VALID_POS:
        p = board.board[pos]

        # # skip blank squares and wrong colour
        if p not in board.ally_pieces:
            continue

        # check if the piece is pinned
        is_pinned = False
        for pin in pins:
            if pin[0] == pos:
                is_pinned = True
                pin_dir = pin[1]

        if p.upper() == "P":
            # pawn forward moves
            for move in MOVE_TABLES[pos][p]:
                target = board.board[move.dest]

                if target == ".":
                    if not is_pinned or pin_dir in (N, S):
                        moves.append(move)
                else:
                    break  # this is needed so that if there is a pawn double move it will be skipped (double pawn move can't jump over piece)

            # pawn attack moves
            for dir, p_moves in MOVE_TABLES[pos][p + "a"].items():
                for move in p_moves:
                    target = board.board[move.dest]

                    if target in board.enemy_pieces:
                        if not is_pinned or pin_dir in (dir, -dir):
                            moves.append(move)

        elif p.upper() in "BRQ":
            # iterate through each direction, add the moves in that direction
            for dir, p_moves in MOVE_TABLES[pos][p.upper()].items():
                if is_pinned and pin_dir not in (dir, -dir):
                    continue

                # loop through every position in those moves
                for move in p_moves:
                    target = board.board[move.dest]

                    # if no piece add the move
                    if target == ".":
                        moves.append(move)
                    else:
                        # if enemy piece add the move
                        if target in board.enemy_pieces:
                            moves.append(move)
                        break  # if friendly or enemy exit the p_moves loop (exiting all moves in this direction)

        elif p.upper() == "N":
            # add all moves the knight can make if it isn't pinned
            if not is_pinned:
                for move in MOVE_TABLES[pos][p.upper()]:
                    target = board.board[move.dest]

                    # add the move if target is blank square or enemy piece
                    if target == "." or target in board.enemy_pieces:
                        moves.append(move)

    return moves


def get_all_captures(board: Board, pins):
    moves = []

    for pos in VALID_POS:
        p = board.board[pos]

        # skip blank squares and wrong colour
        if p not in board.ally_pieces:
            continue

        # check if the piece is pinned
        is_pinned = False
        for pin in pins:
            if pin[0] == pos:
                is_pinned = True
                pin_dir = pin[1]

        if p.upper() == "P":
            for dir, p_moves in MOVE_TABLES[pos][p + "a"].items():
                for move in p_moves:
                    target = board.board[move.dest]

                    if target in board.enemy_pieces:
                        if not is_pinned or pin_dir in (dir, -dir):
                            moves.append(move)

        elif p.upper() in "BRQ":
            # iterate through each direction, add the moves in that direction
            for dir, p_moves in MOVE_TABLES[pos][p.upper()].items():
                if is_pinned and pin_dir not in (dir, -dir):
                    continue

                # loop through every position in those moves
                for move in p_moves:
                    target = board.board[move.dest]

                    if target != ".":
                        # if enemy piece add the move
                        if target in board.enemy_pieces:
                            moves.append(move)
                        break  # if friendly or enemy exit the p_moves loop (exiting all moves in this direction)

        elif p.upper() == "N":
            # add all moves the knight can make if it isn't pinned
            if not is_pinned:
                for move in MOVE_TABLES[pos][p.upper()]:
                    target = board.board[move.dest]

                    # add the move if attacking enemy
                    if target in board.enemy_pieces:
                        moves.append(move)
    return moves


def in_check(board: Board, king_pos: int):
    for dir, positions in LINE_OF_SIGHT[king_pos].items():
        for dist, pos in enumerate(positions):
            # get the piece there
            piece = board.board[pos]
            ptype = piece.upper()

            if piece == ".":
                continue

            if piece in board.ally_pieces:
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

    for pos in LINE_OF_SIGHT_KNIGHT[king_pos]:
        piece = board.board[pos]

        if piece.upper() == "N" and piece in board.enemy_pieces:
            return True

    return False


def get_pins_and_checks(board: Board, king_pos: int):
    pins, checks = [], []

    for dir, positions in LINE_OF_SIGHT[king_pos].items():
        possible_pin = False

        for dist, pos in enumerate(positions):
            # get the piece there
            piece = board.board[pos]
            ptype = piece.upper()

            if piece == ".":
                continue

            # if friendly piece
            if piece in board.ally_pieces:
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

    for pos in LINE_OF_SIGHT_KNIGHT[king_pos]:
        piece = board.board[pos]

        if piece.upper() == "N" and piece in board.enemy_pieces:
            checks.append((pos, dir))

    return pins, checks
