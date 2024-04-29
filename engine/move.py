from __future__ import annotations

from .utils import get_square


class Move:
    def __init__(self, pos: int, dest: int, capture: bool = False, castling: str = "", prom: str = "", double: bool = False, ep: int = 0) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
        self.castling = castling
        self.prom = prom
        self.double = double
        self.ep = ep

    def __eq__(self, other: Move) -> bool:
        return self.pos == other.pos and self.dest == other.dest and self.prom == other.prom

    def __repr__(self) -> str:
        return get_square(self.pos) + get_square(self.dest) + self.prom
