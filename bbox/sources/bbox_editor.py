from abc import ABC

from bbox.sources.bbox_creator import AnyBBox
from bbox.sources.bbox_getter import BBoxGetter


class BBoxEditor(BBoxGetter, ABC):
    def move_basis(self, x: int | float, y: int | float) -> None:
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

    def zero_basis(self) -> None:
        self.x2 = self.w
        self.y2 = self.h
        self.x1 = 0
        self.y1 = 0

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

    def replace_from(self, bbox: AnyBBox) -> None:
        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox: AnyBBox) -> None:
        self.x1 = min(self.x1, bbox.x1)
        self.y1 = min(self.y1, bbox.y1)
        self.x2 = max(self.x2, bbox.x2)
        self.y2 = max(self.y2, bbox.y2)
