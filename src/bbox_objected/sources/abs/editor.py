from ..bbox_editor import BBoxEditor


class AbsBBoxEditor(BBoxEditor):
    def round_coords(self) -> None:
        self._set_coords(round(self.x1), round(self.y1), round(self.x2), round(self.y2))

    def move_basis(self, x: int, y: int) -> None:
        self._set_coords(self.x1 + x, self.y1 + y, self.x2 + x, self.y2 + y)

    def zero_basis(self) -> None:
        self._set_coords(0, 0, self.w, self.h)

    def multiply_by(self, value: float) -> None:
        if value < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        self._set_coords(
            round(self.x1 * value),
            round(self.y1 * value),
            round(self.x2 * value),
            round(self.y2 * value),
        )

    def divide_by(self, value: float) -> None:
        if value <= 0:
            err = "Divisor must be positive"
            raise ValueError(err)
        self._set_coords(
            round(self.x1 / value),
            round(self.y1 / value),
            round(self.x2 / value),
            round(self.y2 / value),
        )
