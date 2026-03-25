from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from ..domain.abs_bbox import AbsBBox

if TYPE_CHECKING:
    from .._typing import ImageLike
    from ..domain.rel_bbox import RelBBox


def _as_abs_coords(bbox: AbsBBox | RelBBox, img: ImageLike) -> tuple[int, int, int, int]:
    if isinstance(bbox, AbsBBox):
        return bbox.as_tuple()

    h, w, *_ = img.shape
    return bbox.as_abs(img_w=w, img_h=h).as_tuple()


def show_on_image(bbox: AbsBBox | RelBBox, img: ImageLike, text: str | None = None) -> None:
    try:
        cv2 = importlib.import_module("cv2")
    except ModuleNotFoundError as exc:
        err = "'OpenCV' is required to use 'show_on_image'"
        raise NotImplementedError(err) from exc

    cv: Any = cv2
    cv_img: Any = img.copy()
    if cv_img.ndim == 2:  # noqa: PLR2004
        cv_img = cv.cvtColor(cv_img, cv.COLOR_GRAY2BGR)  # ty: ignore[no-matching-overload]

    x1, y1, x2, y2 = _as_abs_coords(bbox, img)
    cv.rectangle(cv_img, (x1, y1), (x2, y2), (0, 255, 0))  # ty: ignore[no-matching-overload]
    label = text if text is not None else getattr(bbox, "text", "")
    if label:
        cv.putText(  # ty: ignore[no-matching-overload]
            cv_img,
            label,
            (x1, y1 + 10),
            cv.FONT_ITALIC,
            0.5,
            (0, 0, 255),
            2,
        )

    cv.imshow("bbox_objected_show", cv_img)  # ty: ignore[no-matching-overload]
    cv.waitKey(0)
    cv.destroyWindow("bbox_objected_show")
