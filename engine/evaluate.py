from .board import Board
from .constants import VALID_POS, GAME_PHASE_VALUE, ISOLATED_PAWN_VALUE
from .precalculated_data import MG_TABLES, EG_TABLES, ADJ_PAWN_FILES, PASSED_PAWNS, PASSED_PAWN_VALUE


def evaluate(board: Board) -> int:
    game_phase_value = 0
    mg_value = 0
    eg_value = 0
    value = 0

    for pos in VALID_POS:
        p = board.board[pos]
        if p != ".":
            mg_value += MG_TABLES[p][pos]
            eg_value += EG_TABLES[p][pos]
            game_phase_value += GAME_PHASE_VALUE[p]

            if p.upper() == "P":
                enemy_pawn = "p" if p == "P" else "P"

                # passed pawn detection
                for sq in PASSED_PAWNS[pos][p]:
                    if board.board[sq] == enemy_pawn:
                        break
                else:
                    value += PASSED_PAWN_VALUE[pos][p]

                # isolated pawn detection
                for sq in ADJ_PAWN_FILES[pos]:
                    if p == board.board[sq]:  # if ally pawn
                        break
                else:
                    value += ISOLATED_PAWN_VALUE[p]

    mg_phase = min(game_phase_value, 24)  # in case of early promotion
    eg_phase = 24 - mg_phase
    score = (mg_value * mg_phase + eg_value * eg_phase) // 24 + value

    return score if board.white_move else -score
