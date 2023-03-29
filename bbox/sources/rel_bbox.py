from typing import Sequence

from .bbox_getter import BBoxGetter
from ..types import BBoxKind


class RelBBoxGetter(BBoxGetter):

    def get_abs(self, kind: BBoxKind | str, img_w: int, img_h: int) -> tuple:
        return getattr(self, "get_abs_" + str(kind))(img_w, img_h)

    def get_abs_pascal_voc(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return round(self.x1 * img_w), round(self.y1 * img_h), round(self.x2 * img_w), round(self.y2 * img_h)

    def get_abs_x1y1x2y2(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return self.get_abs_pascal_voc(img_w, img_h)

    def get_abs_coco(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return round(self.x1 * img_w), round(self.y1 * img_h), round(self.w * img_w), round(self.h * img_h)

    def get_abs_x1y1wh(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return self.get_abs_coco(img_w, img_h)

    def get_abs_free_list(self, img_w: int, img_h: int) -> tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return self.abs_tl(img_w, img_h), self.abs_tr(img_w, img_h), self.abs_br(img_w, img_h), self.abs_bl(img_w,
                                                                                                            img_h)

    def get_abs_tl_tr_br_bl(self, img_w: int, img_h: int) -> tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return self.get_abs_free_list(img_w, img_h)

    def get_abs_horizontal_list(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return round(self.x1 * img_w), round(self.x2 * img_w), round(self.y1 * img_h), round(self.y2 * img_h)

    def get_abs_x1x2y1y2(self, img_w: int, img_h: int) -> tuple[int, int, int, int]:
        return self.get_abs_horizontal_list(img_w, img_h)

    def get_abs_mss(self, img_w: int, img_h: int) -> dict[str, int]:
        return {"top": round(self.y1 * img_h), "left": round(self.x1 * img_w), "width": round(self.w * img_w),
                "height": round(self.h * img_h)}

    def abs_w(self, img_w: int) -> int:
        return round((self.x2 - self.x1) * img_w)

    def abs_h(self, img_h: int) -> int:
        return round((self.y2 - self.y1) * img_h)

    def abs_xc(self, img_w: int) -> int:
        return round((self.x1 + self.x2) / 2 * img_w)

    def abs_yc(self, img_h: int) -> int:
        return round((self.y1 + self.y2) / 2 * img_h)

    def abs_area(self, img_w: int, img_h: int) -> int:
        return self.abs_w(img_w) * self.abs_h(img_h)

    def abs_center(self, img_w: int, img_h: int) -> tuple[int, int]:
        return self.abs_xc(img_w), self.abs_yc(img_h)

    def abs_tl(self, img_w: int, img_h: int) -> tuple[int, int]:
        return round(self.x1 * img_w), round(self.y1 * img_h)

    def abs_tr(self, img_w: int, img_h: int) -> tuple[int, int]:
        return round(self.x2 * img_w), round(self.y1 * img_h)

    def abs_br(self, img_w: int, img_h: int) -> tuple[int, int]:
        return round(self.x2 * img_w), round(self.y2 * img_h)

    def abs_bl(self, img_w: int, img_h: int) -> tuple[int, int]:
        return round(self.x1 * img_w), round(self.y2 * img_h)


class RelBBoxEditor(RelBBoxGetter):
    def move_basis(self, x: float, y: float) -> None:
        assert isinstance(x, float) and isinstance(y, float) and (0. <= x <= 1.) and (0. <= y <= 1.)
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

    def zero_basis(self) -> None:
        self.x2 = float(self.w)
        self.y2 = float(self.h)
        self.x1 = 0.
        self.y1 = 0.

    def multiply_by(self, value: int | float):
        self.x1 = self.x1 * value
        self.y1 = self.y1 * value
        self.x2 = self.x2 * value
        self.y2 = self.y2 * value

    def divide_by(self, value: int | float):
        self.x1 = self.x1 / value
        self.y1 = self.y1 / value
        self.x2 = self.x2 / value
        self.y2 = self.y2 / value

    def replace_from(self, bbox) -> None:
        assert isinstance(bbox, RelBBox)

        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox) -> None:
        assert isinstance(bbox, RelBBox)

        self.x1 = min(self.x1, bbox.x1)
        self.y1 = min(self.y1, bbox.y1)
        self.x2 = max(self.x2, bbox.x2)
        self.y2 = max(self.y2, bbox.y2)


class RelBBox(RelBBoxEditor):
    def __init__(
            self,
            coords: Sequence,
            kind: BBoxKind | str = "x1y1x2y2",
            text: str = "",
            score: float = 0.5,
            **kwargs,
    ):
        super().__init__(coords, kind)
        self.text = text
        self.score = score
        self.__dict__.update(kwargs)

    def is_valid(self):
        return ((0. <= self.x1 <= 1.) and (0. <= self.y1 <= 1.) and (0. <= self.x2 <= 1.) and (0. <= self.y2 <= 1.))

    def __repr__(self):
        bbox = f"RelBBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        if text := self.text:
            text = f" - {self.text} ({self.score:.2f})"
        return f"<{bbox}{text}>"
