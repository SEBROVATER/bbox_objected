from collections.abc import Sequence
from typing import Generic, TypeVar

from ..annotations import BBoxKind

T = TypeVar("T", int, float)


class BaseBBox(Generic[T]):
    def __init__(self, coords: Sequence[T], kind: BBoxKind | str) -> None:
        kind = str(kind)
        if kind not in BBoxKind.__members__:
            err = f"Unacceptable bbox kind <{kind}>"
            raise TypeError(err)

        self.x1: T
        self.y1: T
        self.x2: T
        self.y2: T

        getattr(self, "_BaseBBox__create_" + kind)(coords)
        self.is_valid()

    def is_valid(self) -> bool:
        comment = (
            "Invalid coords passed, must be: "
            f"x1({self.x1}) <= x2({self.x2}) and y1({self.y1}) <= y2({self.y2})"
        )
        if not ((self.x1 <= self.x2) and (self.y1 <= self.y2)):
            raise ValueError(comment)
        return True

    def __create_pascal_voc(self, coords: Sequence) -> None:
        self.x1, self.y1, self.x2, self.y2 = coords

    def __create_x1y1x2y2(self, coords: Sequence) -> None:
        self.__create_pascal_voc(coords)

    def __create_coco(self, coords: Sequence) -> None:
        self.x1, self.y1 = coords[:2]
        self.x2, self.y2 = self.x1 + coords[2], self.y1 + coords[3]

    def __create_x1y1wh(self, coords: Sequence) -> None:
        self.__create_coco(coords)

    def __create_free_list(self, coords: Sequence) -> None:
        (self.x1, self.y1), (_, _), (self.x2, self.y2), (_, _) = coords

    def __create_tl_tr_br_bl(self, coords: Sequence) -> None:
        self.__create_free_list(coords)

    def __create_horizontal_list(self, coords: Sequence) -> None:
        self.x1, self.x2, self.y1, self.y2 = coords

    def __create_x1x2y1y2(self, coords: Sequence) -> None:
        self.__create_horizontal_list(coords)

    def __create_winocr(self, coords: dict[str, T]) -> None:
        self.x1, self.y1 = coords["x"], coords["y"]
        self.x2 = self.x1 + coords["width"]
        self.y2 = self.y1 + coords["height"]

    def __create_mss(self, coords: dict[str, T]) -> None:
        self.x1 = coords["left"]
        self.y1 = coords["top"]
        self.x2 = self.x1 + coords["width"]
        self.y2 = self.y1 + coords["height"]

    def __repr__(self) -> str:
        bbox = f"BBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        return f"<{bbox}>"
