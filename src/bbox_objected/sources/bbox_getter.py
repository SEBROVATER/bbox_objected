from __future__ import annotations

from ..annotations import BBoxKind
from .bbox_creator import BaseBBox, Number


class BBoxGetter(BaseBBox):
    def get(self, kind: BBoxKind):  # noqa: ANN201
        if kind == BBoxKind.X1Y1X2Y2:
            return self.get_x1y1x2y2()
        if kind == BBoxKind.X1Y1WH:
            return self.get_x1y1wh()
        if kind == BBoxKind.TL_TR_BR_BL:
            return self.get_tl_tr_br_bl()
        if kind == BBoxKind.X1X2Y1Y2:
            return self.get_x1x2y1y2()
        if kind == BBoxKind.MSS:
            return self.get_mss()
        err = f"Kind <{kind}> does not have a getter"
        raise ValueError(err)

    def get_pascal_voc(self) -> tuple[Number, Number, Number, Number]:
        return self.x1, self.y1, self.x2, self.y2

    def get_x1y1x2y2(self) -> tuple[Number, Number, Number, Number]:
        return self.get_pascal_voc()

    def get_coco(self) -> tuple[Number, Number, Number, Number]:
        return self.x1, self.y1, self.w, self.h

    def get_x1y1wh(self) -> tuple[Number, Number, Number, Number]:
        return self.get_coco()

    def get_free_list(
        self,
    ) -> tuple[
        tuple[Number, Number],
        tuple[Number, Number],
        tuple[Number, Number],
        tuple[Number, Number],
    ]:
        return self.tl, self.tr, self.br, self.bl

    def get_tl_tr_br_bl(
        self,
    ) -> tuple[
        tuple[Number, Number],
        tuple[Number, Number],
        tuple[Number, Number],
        tuple[Number, Number],
    ]:
        return self.get_free_list()

    def get_horizontal_list(self) -> tuple[Number, Number, Number, Number]:
        return self.x1, self.x2, self.y1, self.y2

    def get_x1x2y1y2(self) -> tuple[Number, Number, Number, Number]:
        return self.get_horizontal_list()

    def get_mss(self) -> dict[str, Number]:
        return {"top": self.y1, "left": self.x1, "width": self.w, "height": self.h}

    @property
    def w(self) -> Number:
        return self.x2 - self.x1

    @property
    def h(self) -> Number:
        return self.y2 - self.y1

    @property
    def xc(self) -> float:
        return (float(self.x1) + float(self.x2)) / 2.0

    @property
    def yc(self) -> float:
        return (float(self.y1) + float(self.y2)) / 2.0

    @property
    def area(self) -> Number:
        return self.w * self.h

    @property
    def center(self) -> tuple[float, float]:
        return self.xc, self.yc

    @property
    def tl(self) -> tuple[Number, Number]:
        return self.x1, self.y1

    @property
    def tr(self) -> tuple[Number, Number]:
        return self.x2, self.y1

    @property
    def br(self) -> tuple[Number, Number]:
        return self.x2, self.y2

    @property
    def bl(self) -> tuple[Number, Number]:
        return self.x1, self.y2
