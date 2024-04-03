import unittest
import time

import engine
from .helper_functions import perft


class TestSpeedMoveGen(unittest.TestCase):
    def test_speed_move_gen(self) -> None:
        start = time.time()

        board = engine.Board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - "
        )
        num = perft(board, 4)
        self.assertEqual(num, 4085603)

        print(f"Nodes: {num}")
        print(f"Time: {round(time.time()-start), 3}s")
        print(f"Speed: {round(num/(time.time()-start))} nodes/sec")


if __name__ == "__main__":
    unittest.main()
