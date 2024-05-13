from .board import Board
from .constants import VALID_POS, GAME_PHASE_VALUE, MG_VALUES, N, E, S, W
from .precalculated_data import MG_TABLES, EG_TABLES


def evaluate(board: Board) -> int:
    mg_value = 0
    eg_value = 0
    game_phase_value = 0

    for pos in VALID_POS:
        p = board.board[pos]
        if p != ".":
            mg_value += MG_TABLES[p][pos]
            eg_value += EG_TABLES[p][pos]
            game_phase_value += GAME_PHASE_VALUE[p]
            

    # king safety
    for king_pos, pawn_dir, ally_pawn, enemy_pawn, multiplier in ((board.white_king_pos, N, "P", "p", 1), (board.black_king_pos, S, "p", "P", -1)):
        for side_dir in (W, 0, E): # left, same, right
            # square 1 and square 2 are the square forward (or x2 forward) from the king, left from king, or right from king
            square1 = board.board[king_pos+pawn_dir+side_dir]
            square2 = board.board[king_pos+pawn_dir*2+side_dir]
            
            # if either square is an ally pawn add half of a pawn
            if square1 == ally_pawn or square2 == ally_pawn:
                mg_value += multiplier*MG_VALUES["P"]//2
            
            # if either square is an enemy pawn subtract half of a pawn
            if square1 == enemy_pawn or square2 == enemy_pawn:
                mg_value -= multiplier*MG_VALUES["P"]//2

    # calculate phase of game
    mg_phase = min(game_phase_value, 24)  # in case of early promotion
    eg_phase = 24 - mg_phase
    
    
    score = (mg_value * mg_phase + eg_value * eg_phase) // 24
    return score if board.white_move else -score