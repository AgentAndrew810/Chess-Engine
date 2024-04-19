import time

from .move_gen import move_gen, get_pins_and_checks
from .evaluate import evaluate
from .board import Board
from .move import Move
from .constants import MATE_SCORE


class Engine:
    def search(self, board: Board) -> Move | None:
        start = time.time()

        self.tt = {}
        self.nodes = 0
        eval = 0
            
        # iterative deepening
        for depth in range(1, 1000):
            eval = self.negamax(board, depth, float("-inf"), float("inf"))

            # exit if a mate was found - makes it so the mate is actually played
            # otherwise the mate would just be kept within the depth forever            
            if eval == MATE_SCORE:
                break
            
            if time.time()-start >= 1:
                break

        # get time taken
        time_taken = time.time() - start
        if time_taken == 0:
            speed = self.nodes
        else:
            speed = self.nodes / time_taken
            
        # format eval
        eval = eval if board.white_move else -eval # switch to positive = white winning - negative = black winning rather than perspective of engine
        eval_output = "+" if eval >= 0 else "-" # add positive and negative signs
        eval_output += f"M{depth//2}" if abs(eval) == MATE_SCORE else str(eval) # add M if checkmate
            
        print(f"Nodes: {self.nodes} - Time: {round(time_taken, 3)}s - Speed: {round(speed)}nps - Depth: {depth} - Eval: {eval_output}")
        return self.tt.get(board.zobrist, {"move": None})["move"]

    def move_value(self, move: Move) -> int:
        if move.prom:
            return 0
        elif move.capture:
            return 1
        return 2
    
    def negamax(self, board: Board, depth:int, alpha:float, beta:float) -> float:
        alpha_orig = alpha
        self.nodes += 1
        
        # tt_entry = self.tt.get(board.zobrist)
        # if tt_entry is not None and tt_entry["depth"] >= depth:
        #     if tt_entry["flag"] == "exact":
        #         return tt_entry["value"]
        #     elif tt_entry["flag"] == "lower":
        #         alpha = max(alpha, tt_entry["value"])
        #     elif tt_entry["flag"] == "upper":
        #         beta = min(beta, tt_entry["value"])

            # if alpha >= beta:
            #     return tt_entry["value"]
            
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
                return -MATE_SCORE
            # not in check with no moves -> stalemate -> draw
            else:
                return 0

        if depth == 0:
            return evaluate(board)
        
        best_value = float("-inf")
        best_move = None
        
        for move in moves:
            board.make(move)
            value = -self.negamax(board, depth-1, -beta, -alpha)
            alpha = max(alpha, value)
            board.unmake(move)
            
            if value >= best_value:
                best_value = value
                best_move = move
            
            if alpha >= beta:
                break
            
        # store in transposition table
        new_entry = {"depth": depth, "value": value, "move": best_move}
        if value <= alpha_orig:
            new_entry["flag"] = "upper"
        elif value >= beta:
            new_entry["flag"] = "lower"
        else:
            new_entry["flag"] = "exact"
        self.tt[board.zobrist] = new_entry

        return best_value