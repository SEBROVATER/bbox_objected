from __future__ import annotations

from .bbox_getter import BBoxGetter


class BBoxEditor(BBoxGetter):
    _TYPE_VALIDATION_ERROR = (
        "Can only replace from the same bbox class. "
        "Cast to the same type with an as_* method if intended."
    )

    def _ensure_same_type(self, bbox: object) -> None:
        if not isinstance(bbox, self.__class__):
            raise TypeError(self._TYPE_VALIDATION_ERROR)

    def replace_from(self, bbox: BBoxEditor) -> None:
        self._ensure_same_type(bbox)
        self._set_coords(bbox.x1, bbox.y1, bbox.x2, bbox.y2)

    def update_from(self, bbox: BBoxEditor) -> None:
        self._ensure_same_type(bbox)
        self._set_coords(
            min(self.x1, bbox.x1),
            min(self.y1, bbox.y1),
            max(self.x2, bbox.x2),
            max(self.y2, bbox.y2),
        )
