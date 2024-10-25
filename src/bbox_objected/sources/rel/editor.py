from ..bbox_getter import BBoxGetter


class RelBBoxEditor(BBoxGetter):
    _TYPE_VALIDATION_ERROR = (
        "Can only replace from the same bbox class"
        "Cast to the same type with 'as_' method, "
        "if it is intended"
    )

    def move_basis(self, x: float, y: float) -> None:
        if not ((0.0 <= x <= 1.0) and (0.0 <= y <= 1.0)):
            err = f"Coords must be relative: 0.0<=x({x})<=1.0 and 0.0<=y({y})<=1.0"
            raise ValueError(err)
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

    def zero_basis(self) -> None:
        self.x2 = float(self.w)
        self.y2 = float(self.h)
        self.x1 = 0.0
        self.y1 = 0.0

    def multiply_by(self, value: float) -> None:
        self.x1 *= value
        self.y1 *= value
        self.x2 *= value
        self.y2 *= value

    def divide_by(self, value: float) -> None:
        self.x1 /= value
        self.y1 /= value
        self.x2 /= value
        self.y2 /= value

    def replace_from(self, bbox: "RelBBoxEditor") -> None:
        if not isinstance(bbox, RelBBoxEditor):
            raise TypeError(self._TYPE_VALIDATION_ERROR)

        self.x1 = bbox.x1
        self.y1 = bbox.y1
        self.x2 = bbox.x2
        self.y2 = bbox.y2

    def update_from(self, bbox: "RelBBoxEditor") -> None:
        if not isinstance(bbox, RelBBoxEditor):
            raise TypeError(self._TYPE_VALIDATION_ERROR)

        self.x1 = min(self.x1, bbox.x1)
        self.y1 = min(self.y1, bbox.y1)
        self.x2 = max(self.x2, bbox.x2)
        self.y2 = max(self.y2, bbox.y2)
