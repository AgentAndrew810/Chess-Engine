import unittest
import time

import engine
from .helper_functions import get_testing_data, fast_perft

MAX_NODES = 50000


class TestMoveGen(unittest.TestCase):
    def test_move_gen(self) -> None:
        start = time.time()
        total_nodes = 0

        for fen, depths in get_testing_data():
            board = engine.Board(fen)
            print(f"Searching: {fen}")

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
