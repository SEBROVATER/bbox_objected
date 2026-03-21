from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._typing import ImageLike


class BBoxImgMixin:
    @staticmethod
    def _show_on(x1y1x2y2: tuple[int, int, int, int], img: ImageLike, text: str = "") -> None:
        try:
            cv2 = importlib.import_module("cv2")
        except ModuleNotFoundError as exc:
            err = "'OpenCV' is required to use 'show_on' method"
            raise NotImplementedError(err) from exc
        cv: Any = cv2

        cv_img: Any = img.copy()
        if cv_img.ndim == 2:  # noqa: PLR2004
            cv_img = cv.cvtColor(cv_img, cv.COLOR_GRAY2BGR)  # ty: ignore[no-matching-overload]

        x1, y1, x2, y2 = x1y1x2y2

        cv.rectangle(  # ty: ignore[no-matching-overload]
            cv_img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
        )
        cv.putText(  # ty: ignore[no-matching-overload]
            cv_img,
            text,
            (x1, y1 + 10),
            cv.FONT_ITALIC,
            0.5,
            (0, 0, 255),
            2,
        )

        cv.imshow("bbox_objected_show", cv_img)  # ty: ignore[no-matching-overload]
        cv.waitKey(0)
        cv.destroyWindow("bbox_objected_show")
