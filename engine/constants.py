STARTING_BOARD = (
    " " * 20
    + " rnbqkbnr "
    + " pppppppp "
    + " ........ " * 4
    + " PPPPPPPP "
    + " RNBQKBNR "
    + " " * 20
)

C_OFFSETS = (-10, -1, 1, 10)
D_OFFSETS = (-11, -9, 9, 11)

OFFSETS = {
    "N": (-21, -19, -12, -8, 8, 12, 19, 21),
    "B": D_OFFSETS,
    "R": C_OFFSETS,
    "Q": C_OFFSETS + D_OFFSETS,
    "K": C_OFFSETS + D_OFFSETS,
}
