from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypeAlias, TypeGuard

from .sources.bbox_getter import BBoxGetter

BBoxGetterLike: TypeAlias = BBoxGetter
BBoxInput: TypeAlias = BBoxGetterLike | Sequence[int | float]


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


def get_cos_between(bbox1: BBoxGetterLike, bbox2: BBoxGetterLike, xc: float, yc: float) -> float:
    v1x, v1y = bbox1.xc - xc, bbox1.yc - yc
    v2x, v2y = bbox2.xc - xc, bbox2.yc - yc
    inner = v1x * v2x + v1y * v2y
    norms = math.hypot(v1x, v1y) * math.hypot(v2x, v2y)
    if norms == 0:
        err = "Cannot calculate cosine for zero-length vector"
        raise ValueError(err)
    return inner / norms


def get_IoU(bbox_1: BBoxGetterLike, bbox_2: BBoxGetterLike) -> float:  # noqa: N802
    x1 = max(float(bbox_1.x1), float(bbox_2.x1))
    y1 = max(float(bbox_1.y1), float(bbox_2.y1))
    x2 = min(float(bbox_1.x2), float(bbox_2.x2))
    y2 = min(float(bbox_1.y2), float(bbox_2.y2))

    inter_area = max(x2 - x1, 0.0) * max(y2 - y1, 0.0)
    if inter_area == 0:
        return 0.0

    area1 = float(bbox_1.area)
    area2 = float(bbox_2.area)
    return inter_area / (area1 + area2 - inter_area)


def sort_clockwise(bboxes: Sequence[BBoxGetterLike], xc: float, yc: float) -> list[BBoxGetterLike]:
    return sorted(bboxes, key=lambda bbox: math.atan2(bbox.yc - yc, bbox.xc - xc), reverse=True)


def get_distance(bbox_1: BBoxGetterLike, bbox_2: BBoxGetterLike) -> float:
    return math.dist(bbox_1.center, bbox_2.center)


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
    w = max(0.0, xx2 - xx1)
    h = max(0.0, yy2 - yy1)
    return (w * h) / area_b if area_b else 0.0


def non_max_suppression(
    x1y1x2y2: Sequence[BBoxInput],
    thr: float,
    scores: Sequence[float] | None = None,
) -> list[int]:
    if not (0.0 <= thr <= 1.0):
        err = "thr must be between 0.0 and 1.0"
        raise ValueError(err)

    boxes = _to_boxes(x1y1x2y2)
    if len(boxes) == 0:
        return []

    if scores is not None and len(scores) != len(boxes):
        err = "scores length must match number of boxes"
        raise ValueError(err)

    areas = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in boxes]
    if scores is None:
        idxs = sorted(range(len(boxes)), key=lambda i: (boxes[i][3], areas[i]))
    else:
        idxs = sorted(range(len(boxes)), key=lambda i: float(scores[i]))

    pick: list[int] = []
    while len(idxs) > 0:
        i = idxs.pop()
        pick.append(i)
        idxs = [j for j in idxs if _overlap_ratio(boxes[i], boxes[j], areas[j]) <= thr]

    return pick
