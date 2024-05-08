import time

from .move_gen import move_gen, in_check
from .evaluate import evaluate
from .board import Board
from .move import Move
from .constants import MATE_SCORE, MVV_LVA


class Engine:
    def search(self, board: Board, options: dict[str, int] = {}) -> Move | None:
        window = 100

        self.stopped = False
        self.tt = {}
        self.nodes = 0
        self.start = time.time()

        # time calculaton
        remaining_time = options.get("wtime", 30000) if board.white_move else options.get("btime", 30000)  # defaults to 30 seconds
        increment = options.get("winc", 0) if board.white_move else options.get("binc", 0)
        moves_to_go = options.get("movestogo", 30)
        self.max_time = (remaining_time / moves_to_go + increment) / 1000

        # search with an initial depth of 1
        value = self.negamax(board, 1, -MATE_SCORE - 1, MATE_SCORE + 1, 0)
        best_value = value
        time_taken = max(time.time() - self.start, 0.001)
        print(f"info depth 1 time {round(time_taken*1000)} nodes {self.nodes} score cp {value} nps {round(self.nodes/time_taken)}")

        # iterative deepening until time limit is reached
        for depth in range(2, 1001):
            alpha, beta = value - window, value + window
            value = self.negamax(board, depth, alpha, beta, 0)

            # if value was outside alpha or beta, research with full window
            if (value >= beta or value <= alpha) and not self.stopped:
                value = self.negamax(board, depth, -MATE_SCORE - 1, MATE_SCORE + 1, 0)

            if not self.stopped:
                best_value = value

            time_taken = max(time.time() - self.start, 0.001)
            print(f"info depth {depth} time {round(time_taken*1000)} nodes {self.nodes} score cp {best_value} nps {round(self.nodes/time_taken)} ")

            if self.stopped:
                break

        return self.tt.get(board.hash, {"move": None})["move"]

    def negamax(self, board: Board, depth: int, alpha: int, beta: int, ply: int) -> int:
        alpha_orig = alpha
        self.nodes += 1

        if self.stopped:
            return 0

        if time.time() - self.start > self.max_time:
            self.stopped = True
            return 0

        tt_entry = self.tt.get(board.hash)
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
        moves = sorted(moves, key=lambda move: MVV_LVA[board.board[move.dest]][board.board[move.pos]], reverse=True)

        # move the best move to the front of the list for more cutoffs
        if tt_entry is not None:
            best = tt_entry["move"]
            moves.pop(moves.index(best))
            moves.insert(0, best)

        if len(moves) == 0:
            # determine if in check
            king = "K" if board.white_move else "k"
            king_pos = board.board.index(king)
            checked = in_check(board.board, board.white_move, king_pos)

            # if in check with no moves -> checkmate -> return super low score
            if checked:
                return -MATE_SCORE + ply
            # not in check with no moves -> stalemate -> draw
            else:
                return 0

        if depth == 0:
            self.nodes -= 1  # account for duplicate
            return self.quiescence(board, alpha, beta)

        best_value = -MATE_SCORE - 1
        best_move = None

        for move in moves:
            board.make(move)
            value = -self.negamax(board, depth - 1, -beta, -alpha, ply + 1)
            board.unmake(move)

            if self.stopped:
                return 0

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
        self.tt[board.hash] = new_entry

        return best_value

    def quiescence(self, board: Board, alpha: int, beta: int) -> int:
        self.nodes += 1

        static_eval = evaluate(board)
        if static_eval >= beta:
            return beta

        if alpha < static_eval:
            alpha = static_eval

        # generate moves and sort
        moves = move_gen(board, True)
        moves = sorted(moves, key=lambda move: MVV_LVA[board.board[move.dest]][board.board[move.pos]], reverse=True)

        for move in moves:
            board.make(move)
            score = -self.quiescence(board, -beta, -alpha)
            board.unmake(move)

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha
