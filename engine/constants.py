VERSION = "1.0"

# the fen for the starting position
DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# define directions
N, E, S, W = -10, 1, 10, -1
NE, NW, SE, SW = -9, -11, 11, 9

# the offsets of each piece
OFFSETS = {
    "pra": [NE, NW],  # this is opposite for checking if a pawn checks a king by making a king a pawn
    "Pra": [SE, SW],  # ^^^
    "pa": [SE, SW],  # pawn attack moves
    "Pa": [NE, NW],  # ^^^
    "N": [N + NE, N + NW, S + SE, S + SW, E + NE, E + SE, W + NW, W + SW],
    "B": [NE, NW, SE, SW],
    "R": [N, E, S, W],
    "Q": [N, NE, E, SE, S, SW, W, NW],
    "K": [N, NE, E, SE, S, SW, W, NW],
}

# define pieces
WHITE_PIECES = "PNBRQK"
BLACK_PIECES = "pnbrqk"

# all the pieces a pawn can promote to
PROM_PIECES = ["b", "n", "r", "q"]

# the default positions of the white rooks and black rooks
WKROOK = 98
WQROOK = 91
WHITE_KING = 95
BKROOK = 28
BQROOK = 21
BLACK_KING = 25

# how much a mate is worth (high number but not infinity)
MATE_SCORE = 100000

# the values of pieces
MG_VALUES = {"P": 82, "N": 337, "B": 365, "R": 477, "Q": 1025, "K": 0}
EG_VALUES = {"P": 94, "N": 281, "B": 297, "R": 512, "Q": 936, "K": 0}

# how much weight each piece has towards going to end game phase
GAME_PHASE_VALUE = {"p": 0, "P": 0, "n": 1, "N": 1, "b": 1, "B": 1, "r": 2, "R": 2, "q": 4, "Q": 4, "k": 0, "K": 0}

# all the indices that are actually on the chess board in the list
VALID_POS = [num for start in range(21, 92, 10) for num in range(start, start + 8)]

# values for each move, indexed by [victim][attacker]
# order is as follows Most Valuable Victim -> Least Valuable Victim
# if 2+ pieces can capture a Victim then those moves are sorted by Least Valuable Attacker -> Most Valuable Attacker
MVV_LVA = {
    "q": {"K": 50, "Q": 51, "R": 52, "B": 53, "N": 54, "P": 55},
    "r": {"K": 40, "Q": 41, "R": 42, "B": 43, "N": 44, "P": 45},
    "b": {"K": 30, "Q": 31, "R": 32, "B": 33, "N": 34, "P": 35},
    "n": {"K": 20, "Q": 21, "R": 22, "B": 23, "N": 24, "P": 25},
    "p": {"K": 10, "Q": 11, "R": 12, "B": 13, "N": 14, "P": 15},
    "Q": {"k": 50, "q": 51, "r": 52, "b": 53, "n": 54, "p": 55},
    "R": {"k": 40, "q": 41, "r": 42, "b": 43, "n": 44, "p": 45},
    "B": {"k": 30, "q": 31, "r": 32, "b": 33, "n": 34, "p": 35},
    "N": {"k": 20, "q": 21, "r": 22, "b": 23, "n": 24, "p": 25},
    "P": {"k": 10, "q": 11, "r": 12, "b": 13, "n": 14, "p": 15},
    ".": {"P": 15, "p": 15},  # en passant
}

# piece tables in middlegame
MG_TABLES_2D = {
    "P": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [98, 134, 61, 95, 68, 126, 34, -11],
        [-6, 7, 26, 31, 65, 56, 25, -20],
        [-14, 13, 6, 21, 23, 12, 17, -23],
        [-27, -2, -5, 12, 17, 6, 10, -25],
        [-26, -4, -4, -10, 3, 3, 33, -12],
        [-35, -1, -20, -23, -15, 24, 38, -22],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "R": [
        [32, 42, 32, 51, 63, 9, 31, 43],
        [27, 32, 58, 62, 80, 67, 26, 44],
        [-5, 19, 26, 36, 17, 45, 61, 16],
        [-24, -11, 7, 26, 24, 35, -8, -20],
        [-36, -26, -12, -1, 9, -7, 6, -23],
        [-45, -25, -16, -17, 3, 0, -5, -33],
        [-44, -16, -20, -9, -1, 11, -6, -71],
        [-19, -13, 1, 17, 16, 7, -37, -26],
    ],
    "Q": [
        [-28, 0, 29, 12, 59, 44, 43, 45],
        [-24, -39, -5, 1, -16, 57, 28, 54],
        [-13, -17, 7, 8, 29, 56, 47, 57],
        [-27, -27, -16, -16, -1, 17, -2, 1],
        [-9, -26, -9, -10, -2, -4, 3, -3],
        [-14, 2, -11, -2, -5, 2, 14, 5],
        [-35, -8, 11, 2, 8, 15, -3, 1],
        [-1, -18, -9, 10, -15, -25, -31, -50],
    ],
    "B": [
        [-29, 4, -82, -37, -25, -42, 7, -8],
        [-26, 16, -18, -13, 30, 59, 18, -47],
        [-16, 37, 43, 40, 35, 50, 37, -2],
        [-4, 5, 19, 50, 37, 37, 7, -2],
        [-6, 13, 13, 26, 34, 12, 10, 4],
        [0, 15, 15, 15, 14, 27, 18, 10],
        [4, 15, 16, 0, 7, 21, 33, 1],
        [-33, -3, -14, -21, -13, -12, -39, -21],
    ],
    "N": [
        [-167, -89, -34, -49, 61, -97, -15, -107],
        [-73, -41, 72, 36, 23, 62, 7, -17],
        [-47, 60, 37, 65, 84, 129, 73, 44],
        [-9, 17, 19, 53, 37, 69, 18, 22],
        [-13, 4, 16, 13, 28, 19, 21, -8],
        [-23, -9, 12, 10, 19, 17, 25, -16],
        [-29, -53, -12, -3, -1, 18, -14, -19],
        [-105, -21, -58, -33, -17, -28, -19, -23],
    ],
    "K": [
        [-65, 23, 16, -15, -56, -34, 2, 13],
        [29, -1, -20, -7, -8, -4, -38, -29],
        [-9, 24, 2, -16, -20, 6, 22, -22],
        [-17, -20, -12, -27, -30, -25, -14, -36],
        [-49, -1, -27, -39, -46, -44, -33, -51],
        [-14, -14, -22, -46, -44, -30, -15, -27],
        [1, 7, -8, -64, -43, -16, 9, 8],
        [-15, 36, 12, -54, 8, -28, 24, 14],
    ],
}

# piece tables in endgame
EG_TABLES_2D = {
    "P": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [178, 173, 158, 134, 147, 132, 165, 187],
        [94, 100, 85, 67, 56, 53, 82, 84],
        [32, 24, 13, 5, -2, 4, 17, 17],
        [13, 9, -3, -7, -7, -8, 3, -1],
        [4, 7, -6, 1, 0, -5, -1, -8],
        [13, 8, 8, 10, 13, 0, 2, -7],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "R": [
        [13, 10, 18, 15, 12, 12, 8, 5],
        [11, 13, 13, 11, -3, 3, 8, 3],
        [7, 7, 7, 5, 4, -3, -5, -3],
        [4, 3, 13, 1, 2, 1, -1, 2],
        [3, 5, 8, 4, -5, -6, -8, -11],
        [-4, 0, -5, -1, -7, -12, -8, -16],
        [-6, -6, 0, 2, -9, -9, -11, -3],
        [-9, 2, 3, -1, -5, -13, 4, -20],
    ],
    "Q": [
        [-9, 22, 22, 27, 27, 19, 10, 20],
        [-17, 20, 32, 41, 58, 25, 30, 0],
        [-20, 6, 9, 49, 47, 35, 19, 9],
        [3, 22, 24, 45, 57, 40, 57, 36],
        [-18, 28, 19, 47, 31, 34, 39, 23],
        [-16, -27, 15, 6, 9, 17, 10, 5],
        [-22, -23, -30, -16, -16, -23, -36, -32],
        [-33, -28, -22, -43, -5, -32, -20, -41],
    ],
    "B": [
        [-14, -21, -11, -8, -7, -9, -17, -24],
        [-8, -4, 7, -12, -3, -13, -4, -14],
        [2, -8, 0, -1, -2, 6, 0, 4],
        [-3, 9, 12, 9, 14, 10, 3, 2],
        [-6, 3, 13, 19, 7, 10, -3, -9],
        [-12, -3, 8, 10, 13, 3, -7, -15],
        [-14, -18, -7, -1, 4, -9, -15, -27],
        [-23, -9, -23, -5, -9, -16, -5, -17],
    ],
    "N": [
        [-58, -38, -13, -28, -31, -27, -63, -99],
        [-25, -8, -25, -2, -9, -25, -24, -52],
        [-24, -20, 10, 9, -1, -9, -19, -41],
        [-17, 3, 22, 22, 22, 11, 8, -18],
        [-18, -6, 16, 25, 16, 17, 4, -18],
        [-23, -3, -1, 15, 10, -3, -20, -22],
        [-42, -20, -10, -5, -2, -20, -23, -44],
        [-29, -51, -23, -15, -22, -18, -50, -64],
    ],
    "K": [
        [-74, -35, -18, -18, -11, 15, 4, -17],
        [-12, 17, 14, 17, 17, 38, 23, 11],
        [10, 17, 23, 15, 20, 45, 44, 13],
        [-8, 22, 24, 27, 26, 33, 26, 3],
        [-18, -4, 21, 24, 27, 23, 9, -11],
        [-19, -3, 11, 21, 23, 16, 7, -9],
        [-27, -11, 4, 13, 14, 4, -5, -17],
        [-53, -34, -21, -11, -28, -14, -24, -43],
    ],
}
