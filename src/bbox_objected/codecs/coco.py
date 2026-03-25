from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox
from ..domain.rel_bbox import RelBBox

if TYPE_CHECKING:
    from collections.abc import Sequence


def to_abs_bbox(coords: Sequence[int], text: str = "") -> AbsBBox:
    if len(coords) != 4:  # noqa: PLR2004
        err = "COCO expects 4 values: x, y, w, h"
        raise ValueError(err)
    if not all(isinstance(v, int) for v in coords):
        err = "COCO abs expects integer coords"
        raise TypeError(err)
    x1, y1, w, h = coords
    return AbsBBox(x1, y1, x1 + w, y1 + h, text=text)


def to_rel_bbox(coords: Sequence[float], text: str = "") -> RelBBox:
    if len(coords) != 4:  # noqa: PLR2004
        err = "COCO expects 4 values: x, y, w, h"
        raise ValueError(err)
    x1, y1, w, h = coords
    return RelBBox(x1, y1, x1 + w, y1 + h, text=text)


def from_abs_bbox(bbox: AbsBBox) -> tuple[int, int, int, int]:
    return (bbox.x1, bbox.y1, bbox.w, bbox.h)


def from_rel_bbox(bbox: RelBBox) -> tuple[float, float, float, float]:
    return (bbox.x1, bbox.y1, bbox.w, bbox.h)
