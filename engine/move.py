from __future__ import annotations

from .utils import get_square


class Move:
    def __init__(self, pos: int, dest: int, prom: str = "") -> None:
        self.pos = pos
        self.dest = dest
        self.prom = prom

    def __eq__(self, other: Move) -> bool:
        return self.pos == other.pos and self.dest == other.dest and self.prom == other.prom

    def __repr__(self) -> str:
        return get_square(self.pos) + get_square(self.dest) + self.prom


BLANK_MOVE = Move(-1, -1)
