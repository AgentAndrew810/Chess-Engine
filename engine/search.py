import time

from .move_gen import move_gen, get_pins_and_checks
from .evaluate import evaluate
from .board import Board
from .move import Move
from .constants import MATE_SCORE


class Engine:
    def search(self, board: Board, depth: int = 4) -> Move | None:
        start = time.time()

        self.tt = {}
        self.nodes = 0
        self.returned_tt_nodes = 0
        self.tt_nodes = 0

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
            if alpha >= beta:
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
        print(f"TT Nodes: {self.tt_nodes} - TT Returned Nodes: {self.returned_tt_nodes}")

        return best_move

    def move_value(self, move: Move) -> int:
        if move.prom:
            return 0
        elif move.capture:
            return 1
        return 2

    def negamax(self, board: Board, depth: int, alpha: float, beta: float) -> float:
        alpha_orig = alpha
        self.nodes += 1

        tt_entry = self.tt.get(board.zobrist)
        if tt_entry is not None and tt_entry["depth"] >= depth:
            self.tt_nodes += 1
            if tt_entry["flag"] == "exact":
                self.returned_tt_nodes += 1

                return tt_entry["value"]
            elif tt_entry["flag"] == "lower":
                alpha = max(alpha, tt_entry["value"])
            elif tt_entry["flag"] == "upper":
                beta = min(beta, tt_entry["value"])

            if alpha >= beta:
                return tt_entry["value"]

        moves = move_gen(board)
        moves = sorted(moves, key=lambda x: self.move_value(x))

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

            if alpha >= beta:
                break

        new_entry = {"depth": depth, "value": value}
        if value <= alpha_orig:
            new_entry["flag"] = "upper"
        elif value >= beta:
            new_entry["flag"] = "lower"
        else:
            new_entry["flag"] = "exact"
        self.tt[board.zobrist] = new_entry

        return alpha
