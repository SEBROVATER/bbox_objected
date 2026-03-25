from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox
from ..domain.rel_bbox import RelBBox

if TYPE_CHECKING:
    from collections.abc import Sequence


def _parse_points(points: Sequence[Sequence[float]]) -> tuple[float, float, float, float]:
    if len(points) != 4:  # noqa: PLR2004
        err = "EasyOCR expects 4 points: tl, tr, br, bl"
        raise ValueError(err)
    tl, _, br, _ = points
    if len(tl) < 2 or len(br) < 2:  # noqa: PLR2004
        err = "Each point must include x and y"
        raise ValueError(err)
    return tl[0], tl[1], br[0], br[1]


def to_abs_bbox(points: Sequence[Sequence[int]], text: str = "") -> AbsBBox:
    x1, y1, x2, y2 = _parse_points(points)
    if not all(isinstance(v, int) for v in (x1, y1, x2, y2)):
        err = "EasyOCR abs expects integer coords"
        raise TypeError(err)
    return AbsBBox(int(x1), int(y1), int(x2), int(y2), text=text)


def to_rel_bbox(points: Sequence[Sequence[float]], text: str = "") -> RelBBox:
    x1, y1, x2, y2 = _parse_points(points)
    return RelBBox(float(x1), float(y1), float(x2), float(y2), text=text)


def from_abs_bbox(
    bbox: AbsBBox,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    return (bbox.tl, bbox.tr, bbox.br, bbox.bl)


def from_rel_bbox(
    bbox: RelBBox,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
    return (bbox.tl, bbox.tr, bbox.br, bbox.bl)
