def get_pos(rank: int, file: int, white_pov: bool = True) -> int:
    rank, file = (rank, file) if white_pov else (7 - rank, 7 - file)
    return (rank + 2) * 10 + file + 1


def get_coords(pos: int) -> tuple[int, int]:
    rank, file = divmod(pos, 10)
    return rank - 2, file - 1
