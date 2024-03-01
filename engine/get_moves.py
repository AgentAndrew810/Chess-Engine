from .board import Board


def get_legal_moves(board: Board) -> list[int]:
    return []


def get_moves(board: Board) -> list[int]:
    moves = []

    for pos, piece in board.board:
        # skip blank squares and wrong colour
        if piece in " ." or piece.isupper() != board.white_move:
            continue

    return moves
