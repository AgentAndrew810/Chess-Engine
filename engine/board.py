STARTING_BOARD = (
    " " * 20
    + " rnbqkbnr "
    + " pppppppp "
    + " ........ " * 4
    + " PPPPPPPP "
    + " RNBQKBNR "
    + " " * 20
)


class Board:
    def __init__(self) -> None:
        self.board = STARTING_BOARD
        self.white_move = True
