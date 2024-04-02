import engine


def get_testing_data() -> list[tuple[str, list[tuple[int, int]]]]:
    with open("tests/PerftSuite.txt", "r") as file:
        data = [parse_line(line) for line in file]

    return data


def parse_line(line) -> tuple[str, list[tuple[int, int]]]:
    parts = line.split(";")
    fen = parts[0].strip()

    depths = []
    for item in parts[1:]:
        # get the depth and value
        depth, value = item.split()
        depth = depth.replace("D", "")
        depths.append((int(depth), int(value)))

    return fen, depths


def fast_perft(board: engine.Board, depth: int) -> int:
    if depth == 1:
        return len(engine.move_gen(board))

    num = 0
    for move in engine.move_gen(board):
        board.make(move)
        num += perft(board, depth - 1)
        board.unmake(move)

    return num


def perft(board: engine.Board, depth: int) -> int:
    if depth == 0:
        return 1

    num = 0
    for move in engine.move_gen(board):
        board.make(move)
        num += perft(board, depth - 1)
        board.unmake(move)

    return num


def debug_perft(board: engine.Board, depth: int) -> None:
    total = 0
    for move in engine.move_gen(board):
        board.make(move)
        num = perft(board, depth - 1)
        board.unmake(move)

        total += num
        print(f"Move: {move} - {num}")

    print(f"Total Nodes: {total}")
