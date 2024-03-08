# the default board
STARTING_BOARD = (
    " " * 20
    + " rnbqkbnr "
    + " pppppppp "
    + " ........ " * 4
    + " PPPPPPPP "
    + " RNBQKBNR "
    + " " * 20
)

# define directions
N, E, S, W = -10, 1, 10, -1
NE, NW, SE, SW = N + E, N + W, S + E, S + W

# define piece offsets
OFFSETS = {
    "N": (N + NE, N + NW, S + SE, S + SW, E + NE, E + SE, W + NW, W + SW),
    "B": (NE, NW, SE, SW),
    "R": (N, E, S, W),
    "Q": (N, NE, E, SE, S, SW, W, NW),
    "K": (N, NE, E, SE, S, SW, W, NW),
}
