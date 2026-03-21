from __future__ import annotations

from typing import Generic

from .bbox_creator import T
from .bbox_getter import BBoxGetter


class BBoxEditor(BBoxGetter[T], Generic[T]):
    _TYPE_VALIDATION_ERROR = (
        "Can only replace from the same bbox class"
        "Cast to the same type with 'as_' method, "
        "if it is intended"
    )

    def replace_from(self, bbox: BBoxEditor[T]) -> None:
        if not isinstance(bbox, self.__class__):
            raise TypeError(self._TYPE_VALIDATION_ERROR)
        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox: BBoxEditor[T]) -> None:
        if not isinstance(bbox, self.__class__):
            raise TypeError(self._TYPE_VALIDATION_ERROR)

        self.x1 = self.x1 if self.x1 <= bbox.x1 else bbox.x1  # noqa: FURB136
        self.y1 = self.y1 if self.y1 <= bbox.y1 else bbox.y1  # noqa: FURB136
        self.x2 = bbox.x2 if self.x2 <= bbox.x2 else self.x2  # noqa: FURB136
        self.y2 = bbox.y2 if self.y2 <= bbox.y2 else self.y2  # noqa: FURB136
