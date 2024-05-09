from .constants import N, S, OFFSETS, VALID_POS, PROM_PIECES
from .constants import MG_VALUES, MG_TABLES_2D, EG_VALUES, EG_TABLES_2D
from .move import Move

# reverse piece tables for the black pieces (lowercase letter)
for p in "PRQBKN":
    MG_TABLES_2D[p.lower()] = MG_TABLES_2D[p][::-1]
    EG_TABLES_2D[p.lower()] = EG_TABLES_2D[p][::-1]

# pad middle game piece tables, make them one dimesionsal, add piece values, negate values for black
MG_TABLES, EG_TABLES = {}, {}
for p, table in MG_TABLES_2D.items():
    new_table = [0] * 21
    for row in table:
        if p.isupper():
            new_table.extend([value + MG_VALUES[p] for value in row])
        else:
            new_table.extend([-value - MG_VALUES[p.upper()] for value in row])
        new_table.extend([0] * 2)
    new_table.extend([0] * 19)

    MG_TABLES[p] = new_table

# pad endgame piece tables, make them one dimesionsal, add piece values, negate values for black
EG_TABLES = {}
for p, table in EG_TABLES_2D.items():
    new_table = [0] * 21
    for row in table:
        if p.isupper():
            new_table.extend([value + EG_VALUES[p] for value in row])
        else:
            new_table.extend([-value - EG_VALUES[p.upper()] for value in row])
        new_table.extend([0] * 2)
    new_table.extend([0] * 19)

    EG_TABLES[p] = new_table

# create tables of the moves each piece can make from each position
MOVE_TABLES = {}
LINE_OF_SIGHT = {}
LINE_OF_SIGHT_KNIGHT = {}

for pos in VALID_POS:
    MOVE_TABLES[pos] = {}

    for p, first_rank, last_rank, direction in [("P", 8, 3, N), ("p", 3, 8, S)]:
        # pawn forward moves
        if pos // 10 == first_rank:
            MOVE_TABLES[pos][p] = [Move(pos, pos + direction), Move(pos, pos + direction * 2)]
        elif pos // 10 == last_rank:
            MOVE_TABLES[pos][p] = [Move(pos, pos + direction, prom) for prom in PROM_PIECES]
        else:
            MOVE_TABLES[pos][p] = [Move(pos, pos + direction)] if pos + direction in VALID_POS else []

        # pawn attack moves
        if pos // 10 == last_rank:
            MOVE_TABLES[pos][p + "a"] = {
                dir: [Move(pos, pos + dir, prom) for prom in PROM_PIECES] for dir in OFFSETS[p + "a"] if pos + dir in VALID_POS
            }
        else:
            MOVE_TABLES[pos][p + "a"] = {dir: [Move(pos, pos + dir)] for dir in OFFSETS[p + "a"] if pos + dir in VALID_POS}

    # king and knight moves
    for p in "KN":
        MOVE_TABLES[pos][p] = [Move(pos, pos + dir) for dir in OFFSETS[p] if pos + dir in VALID_POS]

    # bishop, rook, and queen moves
    for p in "BRQ":
        MOVE_TABLES[pos][p] = {}
        for dir in OFFSETS[p]:
            MOVE_TABLES[pos][p][dir] = []

            dest = pos + dir
            while dest in VALID_POS:
                MOVE_TABLES[pos][p][dir].append(Move(pos, dest))
                dest += dir

    # add line of sight for all directions and for knight
    LINE_OF_SIGHT[pos] = {dir: [move.dest for move in MOVE_TABLES[pos]["Q"][dir]] for dir in OFFSETS["Q"]}
    LINE_OF_SIGHT_KNIGHT[pos] = [move.dest for move in MOVE_TABLES[pos]["N"]]