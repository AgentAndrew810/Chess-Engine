from .get_legal_moves import get_legal_moves
from .evaluate import evaluate
from .board import Board
from .move import Move


def search(board: Board) -> Move | None:
    return negamax(board, 2)[1]

def negamax(board, depth):
    moves = get_legal_moves(board)
    
    if depth == 0 or len(moves) == 0:
        return evaluate(board), None
    
    max = -100000
    max_move = None
    
    for move in moves:
        child = board.make_move(move)
        
        score = -negamax(child, depth-1)[0]
        
        if score > max:
            max = score
            max_move = move
            
    return max, max_move