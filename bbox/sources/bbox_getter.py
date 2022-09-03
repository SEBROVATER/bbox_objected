from abc import ABC

from bbox.sources.bbox_creator import BaseBBox
from bbox.types import BBoxKind


class BBoxGetter(BaseBBox, ABC):
    def get(self, kind: BBoxKind | str) -> tuple:
        return getattr(self, "get_" + str(kind))()

    def get_pascal_voc(self) -> tuple:
        return self.x1, self.y1, self.x2, self.y2

    def get_x1y1x2y2(self) -> tuple:
        return self.get_pascal_voc()

    def get_coco(self) -> tuple:
        return self.x1, self.y1, self.w, self.h

    def get_x1y1wh(self) -> tuple:
        return self.get_coco()

    def get_free_list(self) -> tuple:
        return self.tl, self.tr, self.br, self.bl

    def get_tltrbrbl(self) -> tuple:
        return self.get_free_list()

    def get_horizontal_list(self) -> tuple:
        return self.x1, self.x2, self.y1, self.y2

    def get_x1x2y1y2(self) -> tuple:
        return self.get_horizontal_list()

    @property
    def w(self) -> int | float:
        return self.x2 - self.x1

    @property
    def h(self) -> int | float:
        return self.y2 - self.y1

    @property
    def xc(self) -> int | float:
        return (self.x1 + self.x2) / 2

    @property
    def yc(self) -> int | float:
        return (self.y1 + self.y2) / 2

    @property
    def area(self) -> int | float:
        return self.w * self.h

    @property
    def center(self) -> tuple:
        return self.xc, self.yc

    @property
    def tl(self) -> tuple:
        return self.x1, self.y1

    @property
    def tr(self) -> tuple:
        return self.x2, self.y1

    @property
    def br(self) -> tuple:
        return self.x2, self.y2

    @property
    def bl(self) -> tuple:
        return self.x1, self.y2
