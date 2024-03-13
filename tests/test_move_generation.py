import unittest

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
            "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1"
        )
        self.assertEqual(self.get_num_moves(board, 1), 6)
        self.assertEqual(self.get_num_moves(board, 2), 264)
        self.assertEqual(self.get_num_moves(board, 3), 9467)
        self.assertEqual(self.get_num_moves(board, 4), 422333)

        # board = engine.Board.create("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
        # self.assertEqual(self.get_num_moves(board, 1), 44)
        # self.assertEqual(self.get_num_moves(board, 2), 1486)
        # self.assertEqual(self.get_num_moves(board, 3), 62379)

    def test_time(self) -> None:
        board = engine.Board.create("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        num_moves = self.get_num_moves(board, 4)
        self.assertEqual(num_moves, 197281)
