from ..bbox_creator import Number
from ..bbox_editor import BBoxEditor


class RelBBoxEditor(BBoxEditor):
    def move_basis(self, x: float, y: float) -> None:
        self._set_coords(self.x1 + x, self.y1 + y, self.x2 + x, self.y2 + y)

    def zero_basis(self) -> None:
        self._set_coords(0.0, 0.0, self.w, self.h)

    def multiply_by(self, value: float) -> None:
        if value < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        self._set_coords(
            self.x1 * value,
            self.y1 * value,
            self.x2 * value,
            self.y2 * value,
        )

    def divide_by(self, value: float) -> None:
        if value <= 0:
            err = "Divisor must be positive"
            raise ValueError(err)
        self._set_coords(
            self.x1 / value,
            self.y1 / value,
            self.x2 / value,
            self.y2 / value,
        )

    @staticmethod
    def _coerce_coord(value: Number) -> float:
        if isinstance(value, bool):
            err = "Invalid coords passed. Use float coords in range [0, 1]"
            raise TypeError(err)
        return float(value)
