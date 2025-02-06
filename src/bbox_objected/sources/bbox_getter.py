from typing import Generic

from ..annotations import BBoxKind
from .bbox_creator import BaseBBox, T


class BBoxGetter(BaseBBox[T], Generic[T]):
    def get(self, kind: BBoxKind | str) -> tuple:
        return getattr(self, "get_" + str(kind))()

    def get_pascal_voc(
        self,
    ) -> tuple[T, T, T, T]:
        return self.x1, self.y1, self.x2, self.y2

    def get_x1y1x2y2(self) -> tuple[T, T, T, T]:
        return self.get_pascal_voc()

    def get_coco(self) -> tuple[T, T, T, T]:
        return self.x1, self.y1, self.w, self.h

    def get_x1y1wh(self) -> tuple[T, T, T, T]:
        return self.get_coco()

    def get_free_list(
        self,
    ) -> tuple[
        tuple[T, T],
        tuple[T, T],
        tuple[T, T],
        tuple[T, T],
    ]:
        return self.tl, self.tr, self.br, self.bl

    def get_tl_tr_br_bl(
        self,
    ) -> tuple[
        tuple[T, T],
        tuple[T, T],
        tuple[T, T],
        tuple[T, T],
    ]:
        return self.get_free_list()

    def get_horizontal_list(
        self,
    ) -> tuple[T, T, T, T]:
        return self.x1, self.x2, self.y1, self.y2

    def get_x1x2y1y2(self) -> tuple[T, T, T, T]:
        return self.get_horizontal_list()

    def get_mss(self) -> dict[str, T]:
        return {"top": self.y1, "left": self.x1, "width": self.w, "height": self.h}

    @property
    def w(self) -> T:
        return self.x2 - self.x1

    @property
    def h(self) -> T:
        return self.y2 - self.y1

    @property
    def xc(self) -> float:
        return (self.x1 + self.x2) / 2

    @property
    def yc(self) -> float:
        return (self.y1 + self.y2) / 2

    @property
    def area(self) -> T:
        return self.w * self.h

    @property
    def center(self) -> tuple[float, float]:
        return self.xc, self.yc

    @property
    def tl(self) -> tuple[T, T]:
        return self.x1, self.y1

    @property
    def tr(self) -> tuple[T, T]:
        return self.x2, self.y1

    @property
    def br(self) -> tuple[T, T]:
        return self.x2, self.y2

    @property
    def bl(self) -> tuple[T, T]:
        return self.x1, self.y2
