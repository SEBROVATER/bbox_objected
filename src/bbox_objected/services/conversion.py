from __future__ import annotations

from ..domain.abs_bbox import AbsBBox
from ..domain.rel_bbox import RelBBox


def abs_to_rel(bbox: AbsBBox, img_w: int, img_h: int) -> RelBBox:
    if img_w <= 0 or img_h <= 0:
        err = "Image width and height must be positive"
        raise ValueError(err)
    x1, y1, x2, y2 = bbox.as_tuple()
    return RelBBox(x1 / img_w, y1 / img_h, x2 / img_w, y2 / img_h, text=bbox.text)


def rel_to_abs(bbox: RelBBox, img_w: int, img_h: int) -> AbsBBox:
    if img_w <= 0 or img_h <= 0:
        err = "Image width and height must be positive"
        raise ValueError(err)
    x1, y1, x2, y2 = bbox.as_tuple()
    return AbsBBox(
        round(x1 * img_w),
        round(y1 * img_h),
        round(x2 * img_w),
        round(y2 * img_h),
        text=bbox.text,
    )
