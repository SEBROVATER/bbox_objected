from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RectCoords:
    x1: float
    y1: float
    x2: float
    y2: float

    def replace(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
