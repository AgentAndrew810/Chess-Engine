from .board import Board
from .constants import VALID_POS, PIECE_VALUES, MG_TABLES


def evaluate(board: Board, middle_game: bool = True) -> int:
    score = 0

    for pos in VALID_POS:
        p = board.board[pos]

        # skip blank squares
        if p == ".":
            continue

        if p.isupper():
            score += PIECE_VALUES[p]
            score += MG_TABLES[p][pos]
        else:
            score -= PIECE_VALUES[p.upper()]
            score -= MG_TABLES[p][pos]

    return score if board.white_move else -score
