from ..bbox_editor import BBoxEditor


class AbsBBoxEditor(BBoxEditor[int]):
    def round_coords(self) -> None:
        self.x1 = round(self.x1)
        self.y1 = round(self.y1)
        self.x2 = round(self.x2)
        self.y2 = round(self.y2)

    def move_basis(self, x: int, y: int) -> None:
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y

    def zero_basis(self) -> None:
        self.x2 = self.w
        self.y2 = self.h
        self.x1 = 0
        self.y1 = 0

    def multiply_by(self, value: float) -> None:
        self.x1 = round(self.x1 * value)
        self.y1 = round(self.y1 * value)
        self.x2 = round(self.x2 * value)
        self.y2 = round(self.y2 * value)

    def divide_by(self, value: float) -> None:
        self.x1 = round(self.x1 / value)
        self.y1 = round(self.y1 / value)
        self.x2 = round(self.x2 / value)
        self.y2 = round(self.y2 / value)
