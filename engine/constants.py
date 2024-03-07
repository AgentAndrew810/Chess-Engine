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

# define piece offsets
OFFSETS = {
    "N": (
        N * 2 + E,
        N * 2 + W,
        S * 2 + E,
        S * 2 + W,
        E * 2 + N,
        E * 2 + S,
        W * 2 + N,
        W * 2 + S,
    ),
    "B": (N + E, E + S, S + W, W + N),
    "R": (N, E, S, W),
    "Q": (N, N + E, E, E + S, S, S + W, W, W + N),
    "K": (N, N + E, E, E + S, S, S + W, W, W + N),
}
