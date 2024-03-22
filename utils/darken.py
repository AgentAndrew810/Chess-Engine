def darken(colour: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return (
        round(colour[0] * factor),
        round(colour[1] * factor),
        round(colour[2] * factor),
    )
