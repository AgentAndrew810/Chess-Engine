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
    def test_promotion(self) -> None:
        board = engine.Board("7K/P7/8/8/8/8/8/7k w - - 0 1")
        board.make(get_move("a7a8"))
        self.assertEqual(board.hash, board.get_hash())

    def test_castling(self) -> None:
        board = engine.Board("4k3/8/8/8/8/8/8/4K2R w K - 1 1")
        board.make(get_move("e1g1"))
        self.assertEqual(board.hash, board.get_hash())

    def test_ep(self) -> None:
        board = engine.Board("7k/2p5/8/1P6/8/8/8/7K b - - 1 1")
        board.make(get_move("c7c5"))
        board.make(get_move("b5c6"))
        self.assertEqual(board.hash, board.get_hash())

    def test_double(self) -> None:
        board = engine.Board("7k/8/8/8/8/8/1P6/7K w - - 1 1")
        board.make(get_move("b2b4"))
        self.assertEqual(board.hash, board.get_hash())

    def test_capture(self) -> None:
        board = engine.Board("7k/8/8/8/8/8/1q6/Q6K w - - 1 1")
        board.make(get_move("a1b2"))
        self.assertEqual(board.hash, board.get_hash())
