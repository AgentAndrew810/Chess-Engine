import unittest
import engine


def get_move(move_str: str) -> engine.Move:
    pos = engine.get_pos(move_str[:2])
    dest = engine.get_pos(move_str[2:])
    move = engine.Move(pos, dest)

    # add promotion
    if len(move_str) > 4:
        move.prom = move_str[4:]

    return move


class TestHashing(unittest.TestCase):
    def check_equal_hash(self, board: engine.Board, moves1: list[str], moves2: list[str]) -> bool:
        for move in moves1:
            board.make(get_move(move))

        key = board.hash

        for move in reversed(moves1):
            board.unmake(get_move(move))

        for move in reversed(moves2):
            board.make(get_move(move))

        self.assertEqual(key, board.hash)

    def test_simple(self) -> None:
        board = engine.Board()
        moves1 = ["d2d4", "d7d5", "g1f3", "g8f6"]
        moves2 = ["g1f3", "g8f6", "d2d4", "d7d5"]
        self.check_equal_hash(board, moves1, moves2)

    def test_promotion(self) -> None:
        board = engine.Board("8/2k2P2/3Q4/8/8/8/8/7K b - - 0 1")
        moves1 = ["c7d6", "f7f8q", "d6d7", "f8d6"]
        moves2 = []
        self.check_equal_hash(board, moves1, moves2)
