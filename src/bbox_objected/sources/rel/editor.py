from ..bbox_editor import BBoxEditor


class RelBBoxEditor(BBoxEditor[float]):
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
