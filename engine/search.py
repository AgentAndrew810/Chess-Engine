import time

from .move_gen import move_gen, in_check
from .evaluate import evaluate
from .board import Board
from .move import Move, BLANK_MOVE
from .constants import MATE_SCORE, MVV_LVA, EG_VALUES

UPPERBOUND = 1
EXACT = 0
LOWERBOUND = -1

MAX_PLY = 1000


class Engine:
    def search(self, board: Board, options: dict[str, int] = {}, difficulty: str = "NA") -> Move:
        window = EG_VALUES["P"] // 2  # half of pawn

        self.stopped = False
        self.nodes = 0
        self.start = time.time()

        self.tt = {}

        self.first_killers = [BLANK_MOVE for _ in range(MAX_PLY + 1)]
        self.second_killers = [BLANK_MOVE for _ in range(MAX_PLY + 1)]
        self.history_moves = [[[0, 0] for _ in range(120)] for _ in range(120)]  # indexed with [move.pos][move.dest][white_to_move]

        # time calculaton
        remaining_time = options.get("wtime", 30000) if board.white_move else options.get("btime", 30000)  # defaults to 30 seconds
        if difficulty == "NA":
            increment = options.get("winc", 0) if board.white_move else options.get("binc", 0)  # get the increment
            moves_to_go = max(options.get("movestogo", 30), 3)  # get moves till next time control
            move_time = min(
                remaining_time / moves_to_go + increment, remaining_time
            )  # calculate time to move, if it is more than we have set it to how much we have left

            self.max_ply = MAX_PLY
        else:
            move_time = min(remaining_time // 30, 4000)  # no more than 4 seconds

            # set difficulty
            if difficulty == "h":
                self.max_ply = MAX_PLY
            elif difficulty == "m":
                self.max_ply = 5
            else:
                self.max_ply = 2

        self.max_time = move_time / 1000 - 0.01  # convert to seconds and remove part of a second to make sure it responds in time

        # start initial search with a depth of 1
        last_value = self.negamax(board, 1, -MATE_SCORE - 1, MATE_SCORE + 1)
        self.print_info(last_value, 1)

        # iterative deepening until time limit is reached
        for depth in range(2, self.max_ply + 1):
            alpha, beta = last_value - window, last_value + window
            value = self.negamax(board, depth, alpha, beta, 0)

            # if value was outside alpha or beta, research with full window
            if (value >= beta or value <= alpha) and not self.stopped:
                value = self.negamax(board, depth, -MATE_SCORE - 1, MATE_SCORE + 1)

            # update last_value if the search was not cancelled, otherwise the score would always be 0 on the cancelled depth
            if not self.stopped:
                last_value = value

            # print output
            self.print_info(last_value, depth)

            # if the search was cancelled exit loop
            if self.stopped:
                break

        # return the best move
        tt_entry = self.tt.get(board.hash)
        return tt_entry[2] if tt_entry is not None else BLANK_MOVE

    def negamax(self, board: Board, depth: int, alpha: int, beta: int, ply: int = 0, null_move_allowed: bool = True) -> int:
        alpha_orig = alpha

        # if used more than the max time stop search and return 0
        if time.time() - self.start >= self.max_time:
            self.stopped = True
            return 0

        self.nodes += 1

        # transposition table
        tt_entry = self.tt.get(board.hash)
        if tt_entry is not None:
            if tt_entry[0] >= depth:
                if tt_entry[3] == EXACT:
                    return tt_entry[1]
                elif tt_entry[3] == LOWERBOUND:
                    alpha = max(alpha, tt_entry[1])
                elif tt_entry[3] == UPPERBOUND:
                    beta = min(beta, tt_entry[1])

                if alpha >= beta:
                    return tt_entry[1]

            hash_move = tt_entry[2]

        else:
            hash_move = BLANK_MOVE

        # get all legal moves
        moves = move_gen(board)

        # determine if in check
        king_pos = board.wk_pos if board.white_move else board.bk_pos
        checked = in_check(board, king_pos)

        # check extension
        # if the king is in_check, increase depth, this enhances search so that we are only evaluating quiet positions + positions in check usually have really low branching factors
        if checked and depth + ply <= self.max_ply:
            depth += 1

        # null move pruning
        if null_move_allowed and not checked and ply != 0 and depth >= 4:
            board.make_null_move()
            best_value = -self.negamax(board, depth - 4, -beta, -beta + 1, False)
            board.unmake_null_move()

            if best_value >= beta:
                return beta

        # determine if threefold repetion -> draw
        # if the current hash is in the past hash's at least twice
        if board.zobrist_key_history.count(board.hash) >= 2:
            return 0

        # determine if checkmate or stalemate
        if len(moves) == 0:
            # if in check with no moves -> checkmate -> return super low score
            # add ply so the engine perfers more direct (less moves) checkmates
            if checked:
                return -MATE_SCORE + ply
            # not in check with no moves -> stalemate -> draw
            else:
                return 0

        if depth == 0:
            self.nodes -= 1  # account for duplicate
            return self.quiescence(board, alpha, beta)

        # sort moves based on the move value function
        moves = sorted(moves, key=lambda move: self.move_value(board, hash_move, move, ply), reverse=True)

        # set initial values
        best_value = -MATE_SCORE - 1
        best_move = BLANK_MOVE

        # loop through all legal moves
        for move in moves:
            board.make(move)
            value = -self.negamax(board, depth - 1, -beta, -alpha, ply + 1)
            board.unmake(move)

            # return if the search got cancelled
            if self.stopped:
                return 0

            # if a new best value was found, update the best_value and best_move
            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

            # cutoff
            if alpha >= beta:
                # if the move is not a capture move
                if board.board[move.dest] == ".":
                    # if a different killer mvoe is stored and the move is not the hash move, store the move as a killer
                    if move != self.first_killers[ply] and move != hash_move:
                        self.second_killers[ply] = self.first_killers[ply]
                        self.first_killers[ply] = move

                    # history heuristic
                    self.history_moves[move.pos][move.dest][board.white_move] += depth * depth

                break

        # store results in transposition table
        if best_value <= alpha_orig:
            self.tt[board.hash] = (depth, best_value, best_move, UPPERBOUND)
        elif best_value >= beta:
            self.tt[board.hash] = (depth, best_value, best_move, LOWERBOUND)
        else:
            self.tt[board.hash] = (depth, best_value, best_move, EXACT)

        return best_value

    def quiescence(self, board: Board, alpha: int, beta: int) -> int:
        self.nodes += 1

        static_eval = evaluate(board)
        if static_eval >= beta:
            return beta

        alpha = max(alpha, static_eval)

        # generate moves and sort with MVV LVA
        moves = move_gen(board, True)
        moves = sorted(moves, key=lambda move: MVV_LVA[board.board[move.dest]][board.board[move.pos]], reverse=True)

        for move in moves:
            board.make(move)
            score = -self.quiescence(board, -beta, -alpha)
            board.unmake(move)

            if score >= beta:
                return beta

            alpha = max(alpha, score)

        return alpha

    def print_info(self, value: int, depth: int) -> None:
        time_taken = max(time.time() - self.start, 0.001)
        nps = round(self.nodes / time_taken)
        time_taken = round(time_taken * 1000)

        print(f"info depth {depth} time {time_taken} nodes {self.nodes} score cp {value} nps {nps}")

    def move_value(self, board: Board, hash_move: Move, move: Move, ply: int) -> int:
        # if the move is the hash move, score it #1
        if move == hash_move:
            return 100000

        # if the move is a capture, score it with MVV LVA
        elif board.board[move.dest] != ".":
            return 90000 + MVV_LVA[board.board[move.dest]][board.board[move.pos]]

        # if the move is the first killer move
        elif move == self.first_killers[ply]:
            return 80000

        # if the move is the second killer move
        elif move == self.second_killers[ply]:
            return 70000

        # return history value
        else:
            return self.history_moves[move.pos][move.dest][board.white_move]
