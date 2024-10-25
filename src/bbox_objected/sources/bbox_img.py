from typing import Any

try:
    import cv2

    _OPENCV_AVAILABLE = True
    import numpy.typing as npt
except ImportError:
    _OPENCV_AVAILABLE = False


class BBoxImgMixin:
    @staticmethod
    def crop_from(img: Any) -> None:  # noqa: ANN401
        err = "'numpy' is required to use 'crop_from' method"
        raise NotImplementedError(err)

    if _OPENCV_AVAILABLE:

        def show_on(self, img: npt.NDArray, text: str = "") -> None:
            img = img.copy()
            if len(img.shape) == 2:  # noqa: PLR2004
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            if (
                (0.0 <= self.x1 <= 1.0)
                and (0.0 <= self.y1 <= 1.0)
                and (0.0 <= self.x2 <= 1.0)
                and (0.0 <= self.y2 <= 1.0)
            ):
                h, w, *_ = img.shape
                x1, y1, x2, y2 = self.as_abs(w, h).get_pascal_voc()
                cv2.rectangle(img, (round(x1), round(y1)), (round(x2), round(y2)), (0, 255, 0))
                cv2.putText(
                    img,
                    text,
                    (round(x1), round(y1) + 10),
                    cv2.FONT_ITALIC,
                    0.5,
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.rectangle(
                    img,
                    (round(self.x1), round(self.y1)),
                    (round(self.x2), round(self.y2)),
                    (0, 255, 0),
                )
                cv2.putText(
                    img,
                    text,
                    (round(self.x1), round(self.y1) + 10),
                    cv2.FONT_ITALIC,
                    0.5,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("bbox_objected_show", img)
            cv2.waitKey(0)
            cv2.destroyWindow("bbox_objected_show")
    else:

        @staticmethod
        def show_on(*args, **kwargs) -> None:
            err = "'OpenCV' is required to use 'show_on' method"
            raise NotImplementedError(err)
