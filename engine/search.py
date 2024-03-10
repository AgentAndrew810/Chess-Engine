import random

from .get_legal_moves import get_legal_moves
from .board import Board
from .move import Move


def search(board: Board) -> Move:
    return random.choice(get_legal_moves(board))
