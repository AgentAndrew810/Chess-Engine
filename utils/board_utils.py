def get_pos(rank: int, file: int) -> int:
    return (rank + 2) * 10 + file + 1


def get_rank_and_file(pos: int) -> tuple[int, int]:
    rank = pos // 10 - 2
    file = pos % 10 - 1
    return rank, file


def flip_coordinates(rank: int, file: int, white_pov: bool) -> tuple[int, int]:
    return (rank, file) if white_pov else (7 - rank, 7 - file)
