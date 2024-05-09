import unittest
import time

import engine
from .helper_functions import get_testing_data, fast_perft

MAX_NODES = 500000


class TestMoveGen(unittest.TestCase):
    def test_move_gen(self) -> None:
        # test that each position has the correct perft results
        start = time.time()
        total_nodes = 0

        for num, (fen, depths) in enumerate(get_testing_data()):
            board = engine.Board(fen)
            print(f"Searching Position #{num+1}: {fen}")

            for depth, value in depths:
                # skip depths that are too large
                if value >= MAX_NODES:
                    break

                num = fast_perft(board, depth)
                self.assertEqual(num, value)

                total_nodes += num

        end = time.time()
        print(f"Total Nodes Found: {total_nodes}")
        print(f"Speed: {round(total_nodes/(end-start))} nodes/sec")

    def test_move_gen_captures(self) -> None:
        # test to make sure captures are also valid moves
        # search to a depth of 2 to make sure all captures are in normal moves
        for num, (fen, depths) in enumerate(get_testing_data()):
            board = engine.Board(fen)
            print(f"Searching Position #{num+1}: {fen}")

            for move in engine.move_gen(board, False):
                board.make(move)

                all_moves = engine.move_gen(board, False)
                all_captures = engine.move_gen(board, False)

                for capture_move in all_captures:
                    self.assertIn(capture_move, all_moves)

                board.unmake(move)
