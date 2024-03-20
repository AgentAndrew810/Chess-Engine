import unittest

import engine


class TestMoveGeneration(unittest.TestCase):
    def get_num_moves(self, board: engine.Board, depth: int) -> int:
        if depth == 0:
            return 1

        num = 0
        for move in engine.get_legal_moves(board):
            board.make(move)
            num += self.get_num_moves(board, depth - 1)
            board.unmake()

        return num

    def test_position_1(self):
        board = engine.Board(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
        self.assertEqual(self.get_num_moves(board, 1), 20)
        self.assertEqual(self.get_num_moves(board, 2), 400)
        self.assertEqual(self.get_num_moves(board, 3), 8902)
        self.assertEqual(self.get_num_moves(board, 4), 197281)

    def test_position_2(self):
        board = engine.Board(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
        )
        self.assertEqual(self.get_num_moves(board, 1), 48)
        self.assertEqual(self.get_num_moves(board, 2), 2039)
        self.assertEqual(self.get_num_moves(board, 3), 97862)
        self.assertEqual(self.get_num_moves(board, 4), 4085603)

    def test_position_3(self):
        board = engine.Board("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -")
        self.assertEqual(self.get_num_moves(board, 1), 14)
        self.assertEqual(self.get_num_moves(board, 2), 191)
        self.assertEqual(self.get_num_moves(board, 3), 2812)
        self.assertEqual(self.get_num_moves(board, 4), 43238)

    def test_position_4(self):
        board = engine.Board(
            "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
        )
        self.assertEqual(self.get_num_moves(board, 1), 6)
        self.assertEqual(self.get_num_moves(board, 2), 264)
        self.assertEqual(self.get_num_moves(board, 3), 9467)
        self.assertEqual(self.get_num_moves(board, 4), 422333)

    def test_position_5(self):
        board = engine.Board(
            "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
        )
        self.assertEqual(self.get_num_moves(board, 1), 44)
        self.assertEqual(self.get_num_moves(board, 2), 1486)
        self.assertEqual(self.get_num_moves(board, 3), 62379)
        self.assertEqual(self.get_num_moves(board, 4), 2103487)

    def test_position_6(self):
        board = engine.Board(
            "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
        )
        self.assertEqual(self.get_num_moves(board, 1), 46)
        self.assertEqual(self.get_num_moves(board, 2), 2079)
        self.assertEqual(self.get_num_moves(board, 3), 89890)
        self.assertEqual(self.get_num_moves(board, 4), 3894594)

    def test_time(self) -> None:
        board = engine.Board(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
        num_moves = self.get_num_moves(board, 4)
        self.assertEqual(num_moves, 197281)
