DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

# define directions
N, E, S, W = -10, 1, 10, -1
NE, NW, SE, SW = -9, -11, 11, 9

# define piece offsets
OFFSETS = {
    "N": (N + NE, N + NW, S + SE, S + SW, E + NE, E + SE, W + NW, W + SW),
    "B": (NE, NW, SE, SW),
    "R": (N, E, S, W),
    "Q": (N, NE, E, SE, S, SW, W, NW),
    "K": (N, NE, E, SE, S, SW, W, NW),
}

# all the pieces a pawn can promote to
PROM_PIECES = ("b", "n", "r", "q")
