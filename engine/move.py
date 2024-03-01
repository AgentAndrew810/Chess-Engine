class Move:
    def __init__(
        self, old_pos: int, new_pos: int, capture: bool, promotion: bool
    ) -> None:
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.capture = capture
        self.promotion = promotion
