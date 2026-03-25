from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox

if TYPE_CHECKING:
    from .._typing import ImageLike
    from ..domain.rel_bbox import RelBBox


def _as_abs_coords(bbox: AbsBBox | RelBBox, img: ImageLike) -> tuple[int, int, int, int]:
    if isinstance(bbox, AbsBBox):
        return bbox.as_tuple()

    h, w, *_ = img.shape
    return bbox.as_abs(img_w=w, img_h=h).as_tuple()


def crop_from_image(bbox: AbsBBox | RelBBox, img: ImageLike) -> ImageLike:
    x1, y1, x2, y2 = _as_abs_coords(bbox, img)
    return img[y1:y2, x1:x2]
