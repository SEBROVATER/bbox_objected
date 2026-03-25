from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.abs_bbox import AbsBBox

if TYPE_CHECKING:
    from collections.abc import Mapping


def to_abs_bbox(data: Mapping[str, int], text: str = "") -> AbsBBox:
    try:
        left = data["left"]
        top = data["top"]
        width = data["width"]
        height = data["height"]
    except KeyError as exc:
        err = "MSS expects keys: left, top, width, height"
        raise ValueError(err) from exc

    if not all(isinstance(v, int) for v in (left, top, width, height)):
        err = "MSS abs expects integer coords"
        raise TypeError(err)

    return AbsBBox(left, top, left + width, top + height, text=text)


def from_abs_bbox(bbox: AbsBBox) -> dict[str, int]:
    return {"left": bbox.x1, "top": bbox.y1, "width": bbox.w, "height": bbox.h}
