from .board import Board
from .constants import VALID_POS, GAME_PHASE_VALUE, HALF_PAWN
from .precalculated_data import MG_TABLES, EG_TABLES, PAWN_FILES, ADJ_PAWN_FILES, MOVE_TABLES


def evaluate(board: Board) -> int:
    game_phase_value = 0
    mg_value = 0
    eg_value = 0

    for pos in VALID_POS:
        p = board.board[pos]
        if p != ".":
            mg_value += MG_TABLES[p][pos]
            eg_value += EG_TABLES[p][pos]
            game_phase_value += GAME_PHASE_VALUE[p]

            if p.upper() == "P":
                # Doubled Pawn Detection
                for pos2 in PAWN_FILES[pos]:  # loop through all squares in same file
                    if p == board.board[pos2]:  # if it is a pawn of the same colour
                        mg_value += -HALF_PAWN if p == "P" else HALF_PAWN

                # Isolated Pawn Detection
                num_ally_pawns = 0
                for pos2 in ADJ_PAWN_FILES[pos]:  # loop through all squares in adjacent files
                    if p == board.board[pos2]:  # if it is a pawn of the same colour:
                        num_ally_pawns += 1

                if num_ally_pawns == 0:  # if no other pawns of the same colour, give a penalty
                    mg_value += -HALF_PAWN if p == "P" else HALF_PAWN

                # Blocked Pawn Detection
                if len(MOVE_TABLES[pos][p.upper()]) == 0:
                    mg_value += -HALF_PAWN if board.white_move else HALF_PAWN

    mg_phase = min(game_phase_value, 24)  # in case of early promotion
    eg_phase = 24 - mg_phase
    score = (mg_value * mg_phase + eg_value * eg_phase) // 24

    return score if board.white_move else -score
