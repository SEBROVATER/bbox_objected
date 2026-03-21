from __future__ import annotations

import math
from collections.abc import Sequence
from decimal import Decimal
from typing import TYPE_CHECKING, TypeAlias, TypeGuard

if TYPE_CHECKING:
    from . import AbsBBox, RelBBox
from .sources.bbox_getter import BBoxGetter

BBoxGetterLike: TypeAlias = BBoxGetter
BBoxInput: TypeAlias = BBoxGetterLike | Sequence[int | float | Decimal]


def _is_bbox_getter(item: object) -> TypeGuard[BBoxGetterLike]:
    return isinstance(item, BBoxGetter)


def _to_boxes(
    x1y1x2y2: Sequence[BBoxInput],
) -> list[tuple[float, float, float, float]]:
    if len(x1y1x2y2) == 0:
        return []

    if isinstance(x1y1x2y2[0], BBoxGetter):
        boxes: list[tuple[float, float, float, float]] = []
        for item in x1y1x2y2:
            if not _is_bbox_getter(item):
                msg = "Expected all items to be bbox objects of the same input shape."
                raise TypeError(msg)
            x1, y1, x2, y2 = item.get_x1y1x2y2()
            boxes.append((float(x1), float(y1), float(x2), float(y2)))
        return boxes

    boxes = []
    for item in x1y1x2y2:
        if isinstance(item, BBoxGetter):
            msg = "Expected all items to be coordinate sequences of the same input shape."
            raise TypeError(msg)
        if len(item) < 4:  # noqa: PLR2004
            msg = "Each coordinates item must contain at least 4 values: x1, y1, x2, y2."
            raise ValueError(msg)
        boxes.append((float(item[0]), float(item[1]), float(item[2]), float(item[3])))
    return boxes


def _overlap_ratio(
    box_a: tuple[float, float, float, float],
    box_b: tuple[float, float, float, float],
    area_b: float,
) -> float:
    x1_a, y1_a, x2_a, y2_a = box_a
    x1_b, y1_b, x2_b, y2_b = box_b
    xx1 = max(x1_a, x1_b)
    yy1 = max(y1_a, y1_b)
    xx2 = min(x2_a, x2_b)
    yy2 = min(y2_a, y2_b)
    w = max(0.0, xx2 - xx1 + 1.0)
    h = max(0.0, yy2 - yy1 + 1.0)
    return (w * h) / area_b if area_b else 0.0


def get_cos_between(
    bbox1: RelBBox | AbsBBox, bbox2: RelBBox | AbsBBox, xc: float, yc: float
) -> float:
    v1x, v1y = bbox1.xc - xc, bbox1.yc - yc
    v2x, v2y = bbox2.xc - xc, bbox2.yc - yc
    inner = v1x * v2x + v1y * v2y
    norms = math.hypot(v1x, v1y) * math.hypot(v2x, v2y)
    return inner / norms


def get_IoU(bbox_1: RelBBox | AbsBBox, bbox_2: RelBBox | AbsBBox) -> float:  # noqa: N802
    """Calculate Intersection over Union for two Bboxes.

    Returns:
        float

    Raises:
        TypeError: if any bbox argument isn't 'RelBBox | AbsBBox' instance

    """
    x1 = max(float(bbox_1.x1), float(bbox_2.x1))
    y1 = max(float(bbox_1.y1), float(bbox_2.y1))
    x2 = min(float(bbox_1.x2), float(bbox_2.x2))
    y2 = min(float(bbox_1.y2), float(bbox_2.y2))

    inter_area = abs(max((x2 - x1, 0)) * max((y2 - y1), 0))
    if inter_area == 0:
        return 0

    area1 = float(bbox_1.area)
    area2 = float(bbox_2.area)
    return inter_area / (area1 + area2 - inter_area)


def sort_clockwise(bboxes: list, xc: float, yc: float) -> list:
    """Expect to get list of groups of BBoxes or list of BBoxes.

    Returns:
        the same list in sorted order

    """
    try:
        bboxes.sort(
            key=lambda group: math.atan2(group[-1].x2 - xc, group[-1].y1 - yc),
            reverse=True,
        )
    except TypeError:
        bboxes.sort(
            key=lambda group: math.atan2(group.x2 - xc, group.y1 - yc),
            reverse=True,
        )
    return bboxes


def get_distance(bbox_1: RelBBox | AbsBBox, bbox_2: RelBBox | AbsBBox) -> float:
    """Distance between centers of BBox objects.

    Returns:
        float

    """
    return math.dist(bbox_1.center, bbox_2.center)


def non_max_suppression(
    x1y1x2y2: Sequence[BBoxInput],
    thr: float,
) -> list[int]:
    boxes = _to_boxes(x1y1x2y2)
    if len(boxes) == 0:
        return []

    pick: list[int] = []
    areas = [(x2 - x1 + 1.0) * (y2 - y1 + 1.0) for x1, y1, x2, y2 in boxes]
    idxs = sorted(range(len(boxes)), key=lambda i: boxes[i][3])  # TODO: add sorting by area
    while len(idxs) > 0:
        i = idxs.pop()
        pick.append(i)
        idxs = [j for j in idxs if _overlap_ratio(boxes[i], boxes[j], areas[j]) <= thr]
    return pick
