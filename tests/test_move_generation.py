import unittest

import engine

MAX_DEPTH = 4


class TestMoveGen(unittest.TestCase):
    def perft(self, board: engine.Board, depth: int) -> int:
        if depth == 1:
            return len(engine.move_gen(board))

        num = 0
        for move in engine.move_gen(board):
            board.make(move)
            num += self.perft(board, depth - 1)
            board.unmake(move)

        return num

    def debug_perft(self, board: engine.Board, depth: int) -> None:
        total = 0
        for move in engine.move_gen(board):
            board.make(move)
            num = self.perft(board, depth - 1)
            board.unmake(move)

            total += num
            print(f"Move: {move} - {num}")

        print(f"Total Nodes: {total}")

    def load_file(self):
        data = []

        with open("tests/PerftSuite.txt", "r") as file:
            for line in file:
                data.append(self.parse_line(line))

        return data

    def parse_line(self, line) -> tuple[str, list[tuple[int, int]]]:
        parts = line.split(";")
        fen = parts[0].strip()

        depths = []
        for item in parts[1:]:
            # get the depth and value
            depth, value = item.split()
            depth = int(depth.replace("D", ""))
            value = int(value)

            # if the depth is <= max depth add it
            if depth <= MAX_DEPTH:
                depths.append((depth, value))

        return fen, depths

    def test_move_gen(self) -> None:
        for fen, depths in self.load_file():
            print(f"Scanning: {fen}")
            board = engine.Board(fen)

            for depth, value in depths:
                num = self.perft(board, depth)
                self.assertEqual(num, value)
