import random

from .get_moves import get_moves
from .board import Board
from .move import Move


def search(board: Board) -> Move:
    return random.choice(get_moves(board))
