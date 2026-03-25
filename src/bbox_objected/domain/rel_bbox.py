from __future__ import annotations

from typing import TYPE_CHECKING

from .coords import RectCoords
from .validators import validate_rel

if TYPE_CHECKING:
    from collections.abc import Iterable


class RelBBox:  # noqa: PLR0904
    _REL_VALIDATION_ERROR = "Invalid coords passed. Use float coords in range [0, 1]"

    def __init__(self, x1: float, y1: float, x2: float, y2: float, text: str = "") -> None:
        self._coords = RectCoords(float(x1), float(y1), float(x2), float(y2))
        self.text = text
        self._validate()

    @classmethod
    def from_tuple(cls, coords: Iterable[float], text: str = "") -> RelBBox:
        x1, y1, x2, y2 = coords
        return cls(float(x1), float(y1), float(x2), float(y2), text=text)

    def _validate(self) -> None:
        validate_rel(self._coords.x1, self._coords.y1, self._coords.x2, self._coords.y2)

    def _set_coords(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self._coords.replace(float(x1), float(y1), float(x2), float(y2))
        self._validate()

    def _set_single(self, name: str, value: float) -> None:
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
    def x1(self) -> float:
        return float(self._coords.x1)

    @x1.setter
    def x1(self, value: float) -> None:
        self._set_single("x1", value)

    @property
    def y1(self) -> float:
        return float(self._coords.y1)

    @y1.setter
    def y1(self, value: float) -> None:
        self._set_single("y1", value)

    @property
    def x2(self) -> float:
        return float(self._coords.x2)

    @x2.setter
    def x2(self, value: float) -> None:
        self._set_single("x2", value)

    @property
    def y2(self) -> float:
        return float(self._coords.y2)

    @y2.setter
    def y2(self, value: float) -> None:
        self._set_single("y2", value)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2)

    def as_abs(self, img_w: int, img_h: int):  # noqa: ANN201
        if img_w <= 0 or img_h <= 0:
            err = "Image width and height must be positive"
            raise ValueError(err)
        from .abs_bbox import AbsBBox  # noqa: PLC0415

        x1, y1, x2, y2 = self.as_tuple()
        return AbsBBox(
            round(x1 * img_w),
            round(y1 * img_h),
            round(x2 * img_w),
            round(y2 * img_h),
            text=self.text,
        )

    @property
    def w(self) -> float:
        return self.x2 - self.x1

    @property
    def h(self) -> float:
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
    def area(self) -> float:
        return self.w * self.h

    @property
    def tl(self) -> tuple[float, float]:
        return self.x1, self.y1

    @property
    def tr(self) -> tuple[float, float]:
        return self.x2, self.y1

    @property
    def br(self) -> tuple[float, float]:
        return self.x2, self.y2

    @property
    def bl(self) -> tuple[float, float]:
        return self.x1, self.y2

    def move(self, dx: float, dy: float) -> None:
        self._set_coords(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)

    def zero_basis(self) -> None:
        self._set_coords(0.0, 0.0, self.w, self.h)

    def scale(self, factor: float) -> None:
        if factor < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        self._set_coords(
            self.x1 * factor,
            self.y1 * factor,
            self.x2 * factor,
            self.y2 * factor,
        )

    def divide(self, value: float) -> None:
        if value <= 0:
            err = "Divisor must be positive"
            raise ValueError(err)
        self._set_coords(
            self.x1 / value,
            self.y1 / value,
            self.x2 / value,
            self.y2 / value,
        )

    def replace_from(self, other: RelBBox) -> None:
        if not isinstance(other, RelBBox):
            err = "Can only replace from RelBBox"
            raise TypeError(err)
        self._set_coords(other.x1, other.y1, other.x2, other.y2)

    def update_from(self, other: RelBBox) -> None:
        if not isinstance(other, RelBBox):
            err = "Can only update from RelBBox"
            raise TypeError(err)
        self._set_coords(
            min(self.x1, other.x1),
            min(self.y1, other.y1),
            max(self.x2, other.x2),
            max(self.y2, other.y2),
        )

    def __repr__(self) -> str:
        bbox = f"RelBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
