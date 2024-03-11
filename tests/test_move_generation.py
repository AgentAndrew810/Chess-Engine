import unittest
import time

import engine


class TestMoveGeneration(unittest.TestCase):
    def get_num_moves(self, board: engine.Board, depth: int) -> int:
        if depth == 0:
            return 1

        num = 0
        for move in engine.get_legal_moves(board):
            child = board.make_move(move)
            num += self.get_num_moves(child, depth - 1)

        return num

    def test_move_generation(self) -> None:
        board = engine.Board.create("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.assertEqual(self.get_num_moves(board, 1), 20)
        self.assertEqual(self.get_num_moves(board, 2), 400)
        self.assertEqual(self.get_num_moves(board, 3), 8902)
        self.assertEqual(self.get_num_moves(board, 4), 197281)

        board = engine.Board.create(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R"
        )
        self.assertEqual(self.get_num_moves(board, 1), 48)
        self.assertEqual(self.get_num_moves(board, 2), 2039)
        self.assertEqual(self.get_num_moves(board, 3), 97862)
        self.assertEqual(self.get_num_moves(board, 4), 4085603)

    def test_time(self) -> None:
        start = time.time()

        board = engine.Board.create("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        num_moves = self.get_num_moves(board, 4)
        self.assertEqual(num_moves, 197281)

        print(f"Time Taken: {time.time()-start}")
