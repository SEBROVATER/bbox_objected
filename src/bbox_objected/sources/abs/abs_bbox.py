from __future__ import annotations

from typing import TYPE_CHECKING

from ...annotations import BBoxKind
from .editor import AbsBBoxEditor

if TYPE_CHECKING:
    from ..bbox_creator import BBoxCoordsInput, Number


class AbsBBox(AbsBBoxEditor):
    def __init__(
        self,
        coords: BBoxCoordsInput,
        kind: BBoxKind = BBoxKind.X1Y1X2Y2,
        text: str = "",
    ) -> None:
        super().__init__(coords, kind)
        self.text = text

    @staticmethod
    def _coerce_coord(value: Number) -> int:
        if not isinstance(value, int):
            comment = "Invalid coords passed. Use only 'int' coords"
            raise TypeError(comment)
        return value

    def as_rel(self, img_w: int, img_h: int):  # noqa: ANN201
        from ..rel.rel_bbox import RelBBox  # noqa: PLC0415

        if img_w <= 0 or img_h <= 0:
            err = "Image width and height must be positive"
            raise ValueError(err)

        x1, y1, x2, y2 = self.get_x1y1x2y2()
        return RelBBox((x1 / img_w, y1 / img_h, x2 / img_w, y2 / img_h), text=self.text)

    def __repr__(self) -> str:
        bbox = f"AbsBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
