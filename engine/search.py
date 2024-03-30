from .move_gen import move_gen
from .evaluate import evaluate
from .board import Board
from .move import Move


def move_value(move: Move):
    if move.prom:
        return 0
    elif move.capture:
        return 1
    return 2


def search(board: Board, depth: int = 3) -> Move | None:
    moves = move_gen(board)
    moves = sorted(moves, key=lambda x: move_value(x))
    best_move = None

    best_eval = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for move in moves:
        board.make(move)

        eval = -negamax(board, depth - 1, -beta, -alpha)

        if eval > best_eval:
            best_move = move
            best_eval = eval

        board.unmake(move)

        alpha = max(alpha, eval)
        if beta <= alpha:
            break

    return best_move


def negamax(board: Board, depth: int, alpha: float, beta: float) -> float:
    moves = move_gen(board)
    moves = sorted(moves, key=lambda x: move_value(x))

    if depth == 0 or len(moves) == 0:
        return evaluate(board)

    value = float("-inf")

    for move in moves:
        board.make(move)
        value = max(value, -negamax(board, depth - 1, -beta, -alpha))
        alpha = max(alpha, value)
        board.unmake(move)

        if beta <= alpha:
            break

    return value
