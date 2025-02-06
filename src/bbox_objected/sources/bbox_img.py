from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt
    from cv2.typing import MatLike


class BBoxImgMixin:
    @staticmethod
    def __show_on(
        x1y1x2y2: tuple[int, int, int, int], img: npt.NDArray[np.uint8] | MatLike, text: str = ""
    ) -> None:
        try:
            import cv2  # noqa: PLC0415
        except ImportError as exc:
            err = "'OpenCV' is required to use 'show_on' method"
            raise NotImplementedError(err) from exc

        img = img.copy()
        if img.ndim == 2:  # noqa: PLR2004
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        x1, y1, x2, y2 = x1y1x2y2

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
        )
        cv2.putText(
            img,
            text,
            (x1, y1 + 10),
            cv2.FONT_ITALIC,
            0.5,
            (0, 0, 255),
            2,
        )

        cv2.imshow("bbox_objected_show", img)
        cv2.waitKey(0)
        cv2.destroyWindow("bbox_objected_show")
