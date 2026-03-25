from __future__ import annotations

from .coords import RectCoords
from .validators import validate_abs


class AbsBBox:  # noqa: PLR0904
    def __init__(self, x1: int, y1: int, x2: int, y2: int, text: str = "") -> None:
        if not all(isinstance(v, int) and not isinstance(v, bool) for v in (x1, y1, x2, y2)):
            err = "Invalid coords passed. Use only 'int' coords"
            raise TypeError(err)
        self._coords = RectCoords(x1, y1, x2, y2)
        self.text = text
        self._validate()

    def _validate(self) -> None:
        validate_abs(self._coords.x1, self._coords.y1, self._coords.x2, self._coords.y2)

    def _set_coords(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if not all(isinstance(v, int) and not isinstance(v, bool) for v in (x1, y1, x2, y2)):
            err = "Invalid coords passed. Use only 'int' coords"
            raise TypeError(err)
        self._coords.replace(x1, y1, x2, y2)
        self._validate()

    def _set_single(self, name: str, value: int) -> None:
        x1, y1, x2, y2 = self.as_tuple()
        if name == "x1":
            x1 = value
        elif name == "y1":
            y1 = value
        elif name == "x2":
            x2 = value
        elif name == "y2":
            y2 = value
        else:
            raise AttributeError(name)
        self._set_coords(x1, y1, x2, y2)

    @property
    def x1(self) -> int:
        return int(self._coords.x1)

    @x1.setter
    def x1(self, value: int) -> None:
        self._set_single("x1", value)

    @property
    def y1(self) -> int:
        return int(self._coords.y1)

    @y1.setter
    def y1(self, value: int) -> None:
        self._set_single("y1", value)

    @property
    def x2(self) -> int:
        return int(self._coords.x2)

    @x2.setter
    def x2(self, value: int) -> None:
        self._set_single("x2", value)

    @property
    def y2(self) -> int:
        return int(self._coords.y2)

    @y2.setter
    def y2(self, value: int) -> None:
        self._set_single("y2", value)

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (self.x1, self.y1, self.x2, self.y2)

    def as_rel(self, img_w: int, img_h: int):  # noqa: ANN201
        if img_w <= 0 or img_h <= 0:
            err = "Image width and height must be positive"
            raise ValueError(err)
        from .rel_bbox import RelBBox  # noqa: PLC0415

        x1, y1, x2, y2 = self.as_tuple()
        return RelBBox(x1 / img_w, y1 / img_h, x2 / img_w, y2 / img_h, text=self.text)

    @property
    def w(self) -> int:
        return self.x2 - self.x1

    @property
    def h(self) -> int:
        return self.y2 - self.y1

    @property
    def xc(self) -> float:
        return (self.x1 + self.x2) / 2.0

    @property
    def yc(self) -> float:
        return (self.y1 + self.y2) / 2.0

    @property
    def center(self) -> tuple[float, float]:
        return self.xc, self.yc

    @property
    def area(self) -> int:
        return self.w * self.h

    @property
    def tl(self) -> tuple[int, int]:
        return self.x1, self.y1

    @property
    def tr(self) -> tuple[int, int]:
        return self.x2, self.y1

    @property
    def br(self) -> tuple[int, int]:
        return self.x2, self.y2

    @property
    def bl(self) -> tuple[int, int]:
        return self.x1, self.y2

    def move(self, dx: int, dy: int) -> None:
        self._set_coords(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)

    def zero_basis(self) -> None:
        self._set_coords(0, 0, self.w, self.h)

    def scale(self, factor: float) -> None:
        if factor < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        self._set_coords(
            round(self.x1 * factor),
            round(self.y1 * factor),
            round(self.x2 * factor),
            round(self.y2 * factor),
        )

    def replace_from(self, other: AbsBBox) -> None:
        if not isinstance(other, AbsBBox):
            err = "Can only replace from AbsBBox"
            raise TypeError(err)
        self._set_coords(other.x1, other.y1, other.x2, other.y2)

    def update_from(self, other: AbsBBox) -> None:
        if not isinstance(other, AbsBBox):
            err = "Can only update from AbsBBox"
            raise TypeError(err)
        self._set_coords(
            min(self.x1, other.x1),
            min(self.y1, other.y1),
            max(self.x2, other.x2),
            max(self.y2, other.y2),
        )

    def __repr__(self) -> str:
        bbox = f"AbsBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
