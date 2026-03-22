from __future__ import annotations

from enum import Enum


class BBoxKind(str, Enum):
    TL_TR_BR_BL = "tl_tr_br_bl"
    X1X2Y1Y2 = "x1x2y1y2"
    X1Y1X2Y2 = "x1y1x2y2"
    X1Y1WH = "x1y1wh"
    WINOCR = "winocr"
    MSS = "mss"

    def __str__(self) -> str:
        return self.value
