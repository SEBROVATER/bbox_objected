from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeGuard

if TYPE_CHECKING:
    from . import AbsBBox, RelBBox

from .sources.bbox_getter import BBoxGetter


def _is_bbox_getter(item: object) -> TypeGuard[BBoxGetter[int | float]]:
    return isinstance(item, BBoxGetter)


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
    x1 = max(bbox_1.x1, bbox_2.x1)
    y1 = max(bbox_1.y1, bbox_2.y1)
    x2 = min(bbox_1.x2, bbox_2.x2)
    y2 = min(bbox_1.y2, bbox_2.y2)

    inter_area = abs(max((x2 - x1, 0)) * max((y2 - y1), 0))
    if inter_area == 0:
        return 0

    return inter_area / (bbox_1.area + bbox_2.area - inter_area)


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
    x1y1x2y2: Sequence[BBoxGetter[int | float] | Sequence[int | float]],
    thr: float,
) -> list[int]:
    if len(x1y1x2y2) == 0:
        return []

    boxes: list[tuple[float, float, float, float]]
    if isinstance(x1y1x2y2[0], BBoxGetter):
        boxes = []
        for item in x1y1x2y2:
            if not _is_bbox_getter(item):
                msg = "Expected all items to be bbox objects of the same input shape."
                raise TypeError(msg)
            x1, y1, x2, y2 = item.get_x1y1x2y2()
            boxes.append((float(x1), float(y1), float(x2), float(y2)))
    else:
        boxes = []
        for item in x1y1x2y2:
            if isinstance(item, BBoxGetter):
                msg = "Expected all items to be coordinate sequences of the same input shape."
                raise TypeError(msg)
            if len(item) < 4:  # noqa: PLR2004
                msg = "Each coordinates item must contain at least 4 values: x1, y1, x2, y2."
                raise ValueError(msg)
            boxes.append((float(item[0]), float(item[1]), float(item[2]), float(item[3])))

    pick: list[int] = []
    areas = [(x2 - x1 + 1.0) * (y2 - y1 + 1.0) for x1, y1, x2, y2 in boxes]
    idxs = sorted(range(len(boxes)), key=lambda i: boxes[i][3])  # TODO: add sorting by area
    while len(idxs) > 0:
        i = idxs.pop()
        pick.append(i)
        x1_i, y1_i, x2_i, y2_i = boxes[i]
        next_idxs: list[int] = []
        for j in idxs:
            x1_j, y1_j, x2_j, y2_j = boxes[j]
            xx1 = max(x1_i, x1_j)
            yy1 = max(y1_i, y1_j)
            xx2 = min(x2_i, x2_j)
            yy2 = min(y2_i, y2_j)
            w = max(0.0, xx2 - xx1 + 1.0)
            h = max(0.0, yy2 - yy1 + 1.0)
            overlap = (w * h) / areas[j] if areas[j] else 0.0
            if overlap <= thr:
                next_idxs.append(j)
        idxs = next_idxs
    return pick
