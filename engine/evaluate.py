from .board import Board
from .constants import VALID_POS, GAME_PHASE_VALUE
from .precalculated_data import MG_TABLES, EG_TABLES


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

    mg_phase = min(game_phase_value, 24)  # in case of early promotion
    eg_phase = 24 - mg_phase
    score = (mg_value * mg_phase + eg_value * eg_phase) // 24

    return score if board.white_move else -score