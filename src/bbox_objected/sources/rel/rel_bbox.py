from __future__ import annotations

from typing import TYPE_CHECKING

from ...annotations import BBoxKind
from .editor import RelBBoxEditor

if TYPE_CHECKING:
    from ..bbox_creator import BBoxCoordsInput


class RelBBox(RelBBoxEditor):
    _REL_VALIDATION_ERROR = "Invalid coords passed. Use float coords in range [0, 1]"

    def __init__(
        self,
        coords: BBoxCoordsInput,
        kind: BBoxKind = BBoxKind.X1Y1X2Y2,
        text: str = "",
    ) -> None:
        super().__init__(coords, kind)
        self.text = text

    @staticmethod
    def _validate_domain(x1: float, y1: float, x2: float, y2: float) -> None:
        in_range = (
            (0.0 <= x1 <= 1.0) and (0.0 <= y1 <= 1.0) and (0.0 <= x2 <= 1.0) and (0.0 <= y2 <= 1.0)
        )
        if not in_range:
            raise ValueError(RelBBox._REL_VALIDATION_ERROR)

    @staticmethod
    def _scaled_to_int(value: float, size: int) -> int:
        return round(value * size)

    def as_abs(self, img_w: int, img_h: int):  # noqa: ANN201
        from ..abs.abs_bbox import AbsBBox  # noqa: PLC0415

        if img_w <= 0 or img_h <= 0:
            err = "Image width and height must be positive"
            raise ValueError(err)

        x1, y1, x2, y2 = self.get_x1y1x2y2()
        return AbsBBox(
            (
                self._scaled_to_int(float(x1), img_w),
                self._scaled_to_int(float(y1), img_h),
                self._scaled_to_int(float(x2), img_w),
                self._scaled_to_int(float(y2), img_h),
            ),
            text=self.text,
        )

    def __repr__(self) -> str:
        bbox = f"RelBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
