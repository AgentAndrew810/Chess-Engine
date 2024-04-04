import engine
import time


def perft(board: engine.Board, depth: int) -> int:
    if depth == 0:
        return 1

    num = 0
    for move in engine.move_gen(board):
        board.make(move)
        num += perft(board, depth - 1)
        board.unmake(move)

    return num


def test_speed_move_gen() -> None:
    start = time.time()

    board = engine.Board("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ")
    num = perft(board, 4)
    print(num, 4085603, num == 4085603)

    print(f"Nodes: {num}")
    print(f"Time: {round(time.time()-start, 3)}s")
    print(f"Speed: {round(num/(time.time()-start))} nodes/sec")


test_speed_move_gen()
