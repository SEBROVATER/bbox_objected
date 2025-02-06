from __future__ import annotations

from typing import TYPE_CHECKING

from ..bbox_img import BBoxImgMixin
from .editor import AbsBBoxEditor

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np
    import numpy.typing as npt
    from cv2.typing import MatLike

    from ...annotations import BBoxKind


class AbsBBox(BBoxImgMixin, AbsBBoxEditor):
    def __init__(
        self,
        coords: Sequence,
        kind: BBoxKind | str = "x1y1x2y2",
        text: str = "",
    ) -> None:
        super().__init__(coords, kind)
        self.text = text

    def crop_from(self, img: npt.NDArray) -> npt.NDArray:
        return img[self.y1 : self.y2, self.x1 : self.x2]

    def is_valid(self) -> bool:
        comment = "Invalid coords passed. Use only 'int' coords"
        if not (
            isinstance(self.x1, int)
            and isinstance(self.y1, int)
            and isinstance(self.x2, int)
            and isinstance(self.y2, int)
        ):
            raise TypeError(comment)
        return super().is_valid()

    def as_rel(self, img_w: int, img_h: int):  # noqa: ANN201
        from ..rel.rel_bbox import RelBBox  # noqa: PLC0415

        x1, y1, x2, y2 = self.get_x1y1x2y2()
        x1 /= img_w
        y1 /= img_h
        x2 /= img_w
        y2 /= img_h
        return RelBBox((x1, y1, x2, y2), text=self.text)

    def show_on(self, img: npt.NDArray[np.uint8] | MatLike) -> None:
        self.__show_on(self.get_x1y1x2y2(), img, self.text)

    def __repr__(self) -> str:
        bbox = f"AbsBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text}"
        return f"<{bbox}{text}>"
