class DrawnObject:
    _instances = []
    ratio = 21 / 18

    def __init__(self) -> None:
        self._instances.append(self)

    @classmethod
    def set_sizes(cls, screen_width: int, screen_height: int) -> None:
        # if the width is bigger than the ratio, use the height to calculate the width
        if screen_width >= screen_height * cls.ratio:
            height = screen_height
            width = round(height * cls.ratio)
        # otherwise use the width to calculate height
        else:
            width = screen_width
            height = round(width / cls.ratio)

        # use the height and width to calculate other sizes
        cls.padd = round(width / 21)
        cls.square_size = cls.padd * 2
        cls.board_size = cls.square_size * 8
        cls.line_size = round(cls.padd / 10)
        cls.piece_size = cls.square_size - cls.line_size * 2

        # calculate the x_padd and y_padd based on if the height or width was adjusted
        # add extra x_padd or y_padd depending on if the width or height is bigger than ratio
        cls.x_padd = cls.padd + (screen_width - width) // 2
        cls.y_padd = cls.padd + (screen_height - height) // 2

        # if instance has an update method call it
        for instance in cls._instances:
            if hasattr(instance, "update"):
                instance.update()
