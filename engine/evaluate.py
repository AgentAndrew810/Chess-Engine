from utils import get_coords
from .board import Board
from .constants import POS_ON_BOARD, PIECE_VALUES, WMG_TABLES, WEG_TABLES

BMG_TABLES = {}
BEG_TABLES = {}

for p, table in WMG_TABLES.items():
    BMG_TABLES[p.lower()] = [row[::-1] for row in table]

for p, table in WEG_TABLES.items():
    BEG_TABLES[p.lower()] = [row[::-1] for row in table]


def evaluate(board: Board, middle_game: bool = True) -> int:
    score = 0

    for pos in POS_ON_BOARD:
        p = board.board[pos]

        # skip blank squares
        if p in " .":
            continue

        rank, file = get_coords(pos)

        if p.isupper():
            score += PIECE_VALUES[p]

            # add middle or endgame piece table values
            if middle_game:
                score += WMG_TABLES[p][rank][file]
            else:
                score += WEG_TABLES[p][rank][file]
        else:
            score -= PIECE_VALUES[p.upper()]

            # add middle or endgame piece table values
            if middle_game:
                score += BMG_TABLES[p][rank][file]
            else:
                score -= WEG_TABLES[p][rank][file]

    return score if board.white_move else -score
