from ..bbox_editor import BBoxEditor


class RelBBoxEditor(BBoxEditor):
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
        if value < 0:
            err = "Multiplier must be non-negative"
            raise ValueError(err)
        self.x1 = min(max(self.x1 * value, 0.0), 1.0)
        self.y1 = min(max(self.y1 * value, 0.0), 1.0)
        self.x2 = min(max(self.x2 * value, 0.0), 1.0)
        self.y2 = min(max(self.y2 * value, 0.0), 1.0)

    def divide_by(self, value: float) -> None:
        if value <= 0:
            err = "Divisor must be positive"
            raise ValueError(err)
        self.x1 = min(max(self.x1 / value, 0.0), 1.0)
        self.y1 = min(max(self.y1 / value, 0.0), 1.0)
        self.x2 = min(max(self.x2 / value, 0.0), 1.0)
        self.y2 = min(max(self.y2 / value, 0.0), 1.0)
