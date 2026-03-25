from __future__ import annotations


def validate_order(x1: float, y1: float, x2: float, y2: float) -> None:
    if not ((x1 <= x2) and (y1 <= y2)):
        err = f"Invalid coords passed, must be: x1({x1}) <= x2({x2}) and y1({y1}) <= y2({y2})"
        raise ValueError(err)


def validate_abs(x1: float, y1: float, x2: float, y2: float) -> None:
    if not all(isinstance(v, int) for v in (x1, y1, x2, y2)):
        err = "Invalid coords passed. Use only 'int' coords"
        raise TypeError(err)
    validate_order(x1, y1, x2, y2)


def validate_rel(x1: float, y1: float, x2: float, y2: float) -> None:
    if not all(isinstance(v, float) for v in (x1, y1, x2, y2)):
        err = "Invalid coords passed. Use float coords in range [0, 1]"
        raise TypeError(err)
    if not all(0.0 <= v <= 1.0 for v in (x1, y1, x2, y2)):
        err = "Invalid coords passed. Use float coords in range [0, 1]"
        raise ValueError(err)
    validate_order(x1, y1, x2, y2)
