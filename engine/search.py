from .get_legal_moves import get_legal_moves
from .evaluate import evaluate
from .board import Board


def search(board: Board, depth=3):
    moves = get_legal_moves(board)
    best_move = None

    best_eval = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for move in moves:
        child = board.make_move(move)
        eval = -negamax(child, depth - 1, -beta, -alpha)

        if eval > best_eval:
            best_move = move
            best_eval = eval

        alpha = max(alpha, eval)
        if alpha > beta:
            break

    return best_move


def negamax(board: Board, depth, alpha, beta):
    moves = get_legal_moves(board)

    if depth == 0 or len(moves) == 0:
        return evaluate(board)

    value = float("-inf")

    for move in moves:
        child = board.make_move(move)

        value = max(value, -negamax(child, depth - 1, -beta, -alpha))
        alpha = max(alpha, value)

        if alpha >= beta:
            break

    return value
