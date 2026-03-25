from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox
from ..domain.rel_bbox import RelBBox

if TYPE_CHECKING:
    from collections.abc import Sequence


def to_abs_bbox(coords: Sequence[int], text: str = "") -> AbsBBox:
    if len(coords) != 4:  # noqa: PLR2004
        err = "Pascal VOC expects 4 values: x1, y1, x2, y2"
        raise ValueError(err)
    if not all(isinstance(v, int) for v in coords):
        err = "Pascal VOC abs expects integer coords"
        raise TypeError(err)
    x1, y1, x2, y2 = coords
    return AbsBBox(x1, y1, x2, y2, text=text)


def to_rel_bbox(coords: Sequence[float], text: str = "") -> RelBBox:
    if len(coords) != 4:  # noqa: PLR2004
        err = "Pascal VOC expects 4 values: x1, y1, x2, y2"
        raise ValueError(err)
    x1, y1, x2, y2 = coords
    return RelBBox(x1, y1, x2, y2, text=text)


def from_abs_bbox(bbox: AbsBBox) -> tuple[int, int, int, int]:
    return bbox.as_tuple()


def from_rel_bbox(bbox: RelBBox) -> tuple[float, float, float, float]:
    return bbox.as_tuple()
