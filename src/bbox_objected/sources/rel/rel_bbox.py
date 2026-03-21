from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from ..bbox_img import BBoxImgMixin
from .editor import RelBBoxEditor

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..._typing import ImageLike
    from ...annotations import BBoxKind


class RelBBox(RelBBoxEditor, BBoxImgMixin):
    _REL_VALIDATION_ERROR = (
        "Invalid coords passed. Use only float or Decimal coords in range [0, 1]"
    )

    x1: float | Decimal
    y1: float | Decimal
    x2: float | Decimal
    y2: float | Decimal

    def __init__(
        self,
        coords: Sequence[float | Decimal],
        kind: BBoxKind | str = "x1y1x2y2",
        text: str = "",
    ) -> None:
        if all(isinstance(value, Decimal) for value in coords):
            kind_name = str(kind)
            if kind_name not in self._bbox_kinds():
                err = f"Unacceptable bbox kind <{kind_name}>"
                raise TypeError(err)
            getattr(self, "_BaseBBox__create_" + kind_name)(coords)
            self.is_valid()
        else:
            if any(isinstance(value, Decimal) for value in coords):
                raise TypeError(self._REL_VALIDATION_ERROR)
            super().__init__([float(value) for value in coords], kind)
        self.text = text

    @staticmethod
    def _bbox_kinds() -> set[str]:
        from ...annotations import BBoxKind  # noqa: PLC0415

        return set(BBoxKind.__members__.keys())

    @staticmethod
    def _scaled_to_int(value: float | Decimal, size: int) -> int:
        if isinstance(value, Decimal):
            return int(round(value * Decimal(size)))  # noqa: RUF046
        return int(round(value * size))  # noqa: RUF046

    @staticmethod
    def _clamp_01(value: float | Decimal) -> float | Decimal:
        if isinstance(value, Decimal):
            if value < Decimal(0):
                return Decimal(0)
            if value > Decimal(1):
                return Decimal(1)
            return value
        if value < 0.0:
            return 0.0
        if value > 1.0:
            return 1.0
        return value

    @staticmethod
    def _to_decimal(value: float | Decimal) -> Decimal:
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def move_basis(self, x: float | Decimal, y: float | Decimal) -> None:
        if not (type(x) is type(self.x1) and type(y) is type(self.y1)):
            err = "move_basis accepts only values of the same numeric type as bbox coords"
            raise TypeError(err)
        if not ((0 <= x <= 1) and (0 <= y <= 1)):
            err = f"Coords must be relative: 0.0<=x({x})<=1.0 and 0.0<=y({y})<=1.0"
            raise ValueError(err)
        if isinstance(self.x1, Decimal):
            dx = self._to_decimal(x)
            dy = self._to_decimal(y)
            self.x1 = self._to_decimal(self.x1) + dx
            self.x2 = self._to_decimal(self.x2) + dx
            self.y1 = self._to_decimal(self.y1) + dy
            self.y2 = self._to_decimal(self.y2) + dy
            return

        dx = float(x)
        dy = float(y)
        self.x1 = float(self.x1) + dx
        self.x2 = float(self.x2) + dx
        self.y1 = float(self.y1) + dy
        self.y2 = float(self.y2) + dy

    def multiply_by(self, value: float | Decimal) -> None:
        if value < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        if isinstance(self.x1, Decimal):
            factor = self._to_decimal(value)
            self.x1 = self._clamp_01(self._to_decimal(self.x1) * factor)
            self.y1 = self._clamp_01(self._to_decimal(self.y1) * factor)
            self.x2 = self._clamp_01(self._to_decimal(self.x2) * factor)
            self.y2 = self._clamp_01(self._to_decimal(self.y2) * factor)
            return

        factor = float(value)
        self.x1 = self._clamp_01(float(self.x1) * factor)
        self.y1 = self._clamp_01(float(self.y1) * factor)
        self.x2 = self._clamp_01(float(self.x2) * factor)
        self.y2 = self._clamp_01(float(self.y2) * factor)

    def divide_by(self, value: float | Decimal) -> None:
        if value <= 0:
            err = "Divisor must be positive"
            raise ValueError(err)
        if isinstance(self.x1, Decimal):
            factor = self._to_decimal(value)
            self.x1 = self._clamp_01(self._to_decimal(self.x1) / factor)
            self.y1 = self._clamp_01(self._to_decimal(self.y1) / factor)
            self.x2 = self._clamp_01(self._to_decimal(self.x2) / factor)
            self.y2 = self._clamp_01(self._to_decimal(self.y2) / factor)
            return

        factor = float(value)
        self.x1 = self._clamp_01(float(self.x1) / factor)
        self.y1 = self._clamp_01(float(self.y1) / factor)
        self.x2 = self._clamp_01(float(self.x2) / factor)
        self.y2 = self._clamp_01(float(self.y2) / factor)

    def crop_from(self, img: ImageLike) -> ImageLike:
        h, w, *_ = img.shape
        x1 = self._scaled_to_int(self.x1, w)
        x2 = self._scaled_to_int(self.x2, w)
        y1 = self._scaled_to_int(self.y1, h)
        y2 = self._scaled_to_int(self.y2, h)

        return img[y1:y2, x1:x2]

    def is_valid(self) -> bool:
        values = (self.x1, self.y1, self.x2, self.y2)
        if len({type(v) for v in values}) != 1:
            raise TypeError(self._REL_VALIDATION_ERROR)

        low = Decimal(0) if isinstance(self.x1, Decimal) else 0.0
        high = Decimal(1) if isinstance(self.x1, Decimal) else 1.0
        if not (
            (low <= self.x1 <= high)
            and (low <= self.y1 <= high)
            and (low <= self.x2 <= high)
            and (low <= self.y2 <= high)
        ):
            raise ValueError(self._REL_VALIDATION_ERROR)

        return super().is_valid()

    def as_abs(self, img_w: int, img_h: int):  # noqa: ANN201
        from ..abs.abs_bbox import AbsBBox  # noqa: PLC0415

        x1, y1, x2, y2 = self.get_x1y1x2y2()
        x1 = self._scaled_to_int(x1, img_w)
        y1 = self._scaled_to_int(y1, img_h)
        x2 = self._scaled_to_int(x2, img_w)
        y2 = self._scaled_to_int(y2, img_h)
        return AbsBBox((x1, y1, x2, y2), text=self.text)

    def show_on(self, img: ImageLike) -> None:
        h, w, *_ = img.shape
        self._show_on(self.as_abs(img_w=w, img_h=h).get_x1y1x2y2(), img, self.text)

    def __repr__(self) -> str:
        bbox = f"RelBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
