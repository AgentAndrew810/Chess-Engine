files = "abcdefgh"
ranks = "87654321"


def get_pos(square: str) -> int:
    rank = ranks.index(square[0])
    file = files.index(square[1])
    return (rank + 2) * 10 + file + 1


def get_square(pos: int) -> str:
    rank, file = divmod(pos, 10)
    return files[file - 1] + ranks[rank - 2]
