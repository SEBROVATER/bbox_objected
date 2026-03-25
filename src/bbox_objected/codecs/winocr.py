from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox

if TYPE_CHECKING:
    from collections.abc import Mapping


def to_abs_bbox(data: Mapping[str, int], text: str = "") -> AbsBBox:
    try:
        x = data["x"]
        y = data["y"]
        w = data["width"]
        h = data["height"]
    except KeyError as exc:
        err = "WinOCR expects keys: x, y, width, height"
        raise ValueError(err) from exc

    if not all(isinstance(v, int) for v in (x, y, w, h)):
        err = "WinOCR abs expects integer coords"
        raise TypeError(err)

    return AbsBBox(x, y, x + w, y + h, text=text)


def from_abs_bbox(bbox: AbsBBox) -> dict[str, int]:
    return {"x": bbox.x1, "y": bbox.y1, "width": bbox.w, "height": bbox.h}
