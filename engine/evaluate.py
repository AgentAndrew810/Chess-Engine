from utils import get_coords
from .board import Board
from .constants import POS_ON_BOARD, PIECE_VALUES, MG_PIECE_TABLES, EG_PIECE_TABLES

BMG_PIECE_TABLES = {}
BEG_PIECE_TABLES = {}

for p, table in MG_PIECE_TABLES.items():
    BMG_PIECE_TABLES[p.lower()] = [row[::-1] for row in table]

for p, table in EG_PIECE_TABLES.items():
    BEG_PIECE_TABLES[p.lower()] = [row[::-1] for row in table]


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
                score += MG_PIECE_TABLES[p][rank][file]
            else:
                score += EG_PIECE_TABLES[p][rank][file]
        else:
            score -= PIECE_VALUES[p.upper()]

            # add middle or endgame piece table values
            if middle_game:
                score += BMG_PIECE_TABLES[p][rank][file]
            else:
                score -= EG_PIECE_TABLES[p][rank][file]

    return score if board.white_move else -score
