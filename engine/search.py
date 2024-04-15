import time

from .move_gen import move_gen, get_pins_and_checks
from .evaluate import evaluate
from .board import Board
from .move import Move
from .constants import MATE_SCORE


class Engine:
    def search(self, board: Board, depth: int = 4) -> Move | None:
        start = time.time()
        self.nodes = 0

        moves = move_gen(board)
        moves = sorted(moves, key=lambda x: self.move_value(x))
        best_move = None

        best_eval = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for move in moves:
            board.make(move)

            eval = -self.negamax(board, depth - 1, -beta, -alpha)

            if eval > best_eval:
                best_move = move
                best_eval = eval

            board.unmake(move)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        time_taken = time.time() - start
        if time_taken == 0:
            speed = self.nodes
        else:
            speed = self.nodes / time_taken

        if best_eval > 0:
            eval = f"Computer is up {round(best_eval/100, 2)}"
        else:
            eval = f"Player is up {round(-best_eval/100, 2)}"

        print(f"Time Taken: {round(time_taken, 3)}s - Speed: {round(speed)}nps - Total Nodes: {self.nodes} - Eval: {eval}")

        return best_move

    def move_value(self, move: Move) -> int:
        if move.prom:
            return 0
        elif move.capture:
            return 1
        return 2

    def negamax(self, board: Board, depth: int, alpha: float, beta: float) -> float:
        moves = move_gen(board)
        moves = sorted(moves, key=lambda x: self.move_value(x))

        self.nodes += 1

        if len(moves) == 0:
            # determine if in check
            king = "K" if board.white_move else "k"
            king_pos = board.board.index(king)
            in_check, _, _ = get_pins_and_checks(board.board, board.white_move, king_pos)

            # if in check with no moves -> checkmate -> return super low score
            if in_check:
                return -MATE_SCORE - depth
            # not in check with no moves -> stalemate -> draw
            else:
                return 0

        if depth == 0:
            return evaluate(board)

        value = float("-inf")

        for move in moves:
            board.make(move)
            value = -self.negamax(board, depth - 1, -beta, -alpha)
            alpha = max(alpha, value)
            board.unmake(move)

            if beta <= alpha:
                break

        return alpha
