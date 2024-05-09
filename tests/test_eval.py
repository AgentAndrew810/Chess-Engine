import unittest

import engine
from .helper_functions import get_testing_data


class TestEval(unittest.TestCase):
    def test_eval(self) -> None:
        # test that after a move the eval is opposite for black
        for fen, _ in get_testing_data():
            board = engine.Board(fen)
            eval = engine.evaluate(board)
            board.white_move = not board.white_move
            self.assertEqual(-eval, engine.evaluate(board))

    def test_starting_eval(self) -> None:
        # test that the starting eval is 0
        board = engine.Board()
        self.assertEqual(engine.evaluate(board), 0)
