import time

from .move_gen import move_gen, get_pins_and_checks
from .evaluate import evaluate
from .board import Board
from .move import Move
from .constants import MATE_SCORE

MAX_TIME = 2


class Engine:
    def search(self, board: Board) -> Move | None:
        start = time.time()
        self.tt = {}
        self.nodes = 0
        
        for depth in range(1, 1000):
            eval = self.negamax(board, depth, float("-inf"), float("inf"), 0)
            
            if time.time() - start > MAX_TIME:
                break        

        # get time taken and speed
        time_taken = time.time() - start
        if time_taken == 0:
            speed = self.nodes
        else:
            speed = self.nodes / time_taken

        # format eval
        eval = eval if board.white_move else -eval  # switch from perspective of engine to perspective of white
        eval_output = f"+{eval}" if eval >= 0 else str(eval)  # add positive and negative signs + convert to string

        print(f"Nodes: {self.nodes} - Time: {round(time_taken, 3)}s - Speed: {round(speed)}nps - Depth: {depth} - Eval: {eval_output}")

        return self.tt.get(board.zobrist, {"move": None})["move"]
    
    def move_value(self, move: Move) -> int:
        if move.prom:
            return 1
        elif move.capture:
            return 1
        return 2

    def negamax(self, board: Board, depth: int, alpha: float, beta: float, ply: int) -> float:
        alpha_orig = alpha
        self.nodes += 1

        tt_entry = self.tt.get(board.zobrist)
        if tt_entry is not None and tt_entry["depth"] >= depth:
            if tt_entry["flag"] == "exact":
                return tt_entry["value"]
            elif tt_entry["flag"] == "lower":
                alpha = max(alpha, tt_entry["value"])
            elif tt_entry["flag"] == "upper":
                beta = min(beta, tt_entry["value"])

            if alpha >= beta:
                return tt_entry["value"]

        # get and sort moves
        moves = move_gen(board)
        moves = sorted(moves, key=lambda x: self.move_value(x))

        if len(moves) == 0:
            # determine if in check
            king = "K" if board.white_move else "k"
            king_pos = board.board.index(king)
            in_check, _, _ = get_pins_and_checks(board.board, board.white_move, king_pos)

            # if in check with no moves -> checkmate -> return super low score
            if in_check:
                return -MATE_SCORE + ply
            # not in check with no moves -> stalemate -> draw
            else:
                return 0

        if depth == 0:
            return evaluate(board)

        best_value = float("-inf")
        best_move = None

        for move in moves:
            board.make(move)
            value = -self.negamax(board, depth - 1, -beta, -alpha, ply + 1)
            board.unmake(move)

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        # store in transposition table
        new_entry = {"depth": depth, "value": best_value, "move": best_move}
        if best_value <= alpha_orig:
            new_entry["flag"] = "upper"
        elif best_value >= beta:
            new_entry["flag"] = "lower"
        else:
            new_entry["flag"] = "exact"
        self.tt[board.zobrist] = new_entry

        return best_value
