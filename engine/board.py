from .constants import STARTING_BOARD


class Board:
    def __init__(self) -> None:
        self.board = STARTING_BOARD
        self.white_move = True