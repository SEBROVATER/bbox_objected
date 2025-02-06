from typing import Generic, Self

from .bbox_creator import T
from .bbox_getter import BBoxGetter


class BBoxEditor(BBoxGetter[T], Generic[T]):
    _TYPE_VALIDATION_ERROR = (
        "Can only replace from the same bbox class"
        "Cast to the same type with 'as_' method, "
        "if it is intended"
    )

    def replace_from(self, bbox: Self) -> None:
        if not isinstance(bbox, self.__class__):
            raise TypeError(self._TYPE_VALIDATION_ERROR)
        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox: Self) -> None:
        if not isinstance(bbox, self.__class__):
            raise TypeError(self._TYPE_VALIDATION_ERROR)

        self.x1 = min(self.x1, bbox.x1)
        self.y1 = min(self.y1, bbox.y1)
        self.x2 = max(self.x2, bbox.x2)
        self.y2 = max(self.y2, bbox.y2)
