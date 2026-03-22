from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

from ..annotations import BBoxKind

Number: TypeAlias = int | float
LinearCoords: TypeAlias = Sequence[Number]
PointCoords: TypeAlias = Sequence[Number]
FreeListCoords: TypeAlias = Sequence[PointCoords]
MappingCoords: TypeAlias = dict[str, Number]


BBoxCoordsInput: TypeAlias = LinearCoords | FreeListCoords | MappingCoords


def _require_number(value: object, *, message: str) -> Number:
    if isinstance(value, bool):
        raise TypeError(message)
    if isinstance(value, (int, float)):
        return value
    raise TypeError(message)


def _parse_linear(
    coords: BBoxCoordsInput, *, message: str
) -> tuple[Number, Number, Number, Number]:
    if isinstance(coords, dict):
        raise TypeError(message)
    if len(coords) != 4:  # noqa: PLR2004
        err = "Expected exactly 4 coordinates"
        raise ValueError(err)

    values: list[Number] = []
    for value in coords:
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            raise TypeError(message)
        values.append(_require_number(value, message=message))
    return values[0], values[1], values[2], values[3]


def _parse_free_list(coords: BBoxCoordsInput) -> tuple[Number, Number, Number, Number]:
    msg = "tl_tr_br_bl kind expects 4 points with numeric coords"
    if isinstance(coords, dict):
        raise TypeError(msg)
    if len(coords) != 4:  # noqa: PLR2004
        err = "tl_tr_br_bl kind expects exactly 4 points"
        raise ValueError(err)

    points: list[tuple[Number, Number]] = []
    for point in coords:
        if not (isinstance(point, Sequence) and not isinstance(point, (str, bytes))):
            raise TypeError(msg)
        if len(point) < 2:  # noqa: PLR2004
            err = "Each point must include x and y"
            raise ValueError(err)
        points.append(
            (
                _require_number(point[0], message=msg),
                _require_number(point[1], message=msg),
            )
        )

    x1, y1 = points[0]
    x2, y2 = points[2]
    return x1, y1, x2, y2


def _require_mapping(coords: BBoxCoordsInput, *, message: str) -> MappingCoords:
    if not isinstance(coords, dict):
        raise TypeError(message)

    normalized: MappingCoords = {}
    for key, value in coords.items():
        if not isinstance(key, str):
            raise TypeError(message)
        normalized[key] = _require_number(value, message=message)
    return normalized


def _parse_winocr(coords: MappingCoords) -> tuple[Number, Number, Number, Number]:
    msg = "winocr kind requires x, y, width, height keys"

    try:
        x1 = _require_number(coords["x"], message=msg)
        y1 = _require_number(coords["y"], message=msg)
        w = _require_number(coords["width"], message=msg)
        h = _require_number(coords["height"], message=msg)
    except KeyError as exc:
        err = "winocr kind requires x, y, width, height keys"
        raise ValueError(err) from exc

    return x1, y1, x1 + w, y1 + h


def _parse_mss(coords: MappingCoords) -> tuple[Number, Number, Number, Number]:
    msg = "mss kind requires left, top, width, height keys"

    try:
        x1 = _require_number(coords["left"], message=msg)
        y1 = _require_number(coords["top"], message=msg)
        w = _require_number(coords["width"], message=msg)
        h = _require_number(coords["height"], message=msg)
    except KeyError as exc:
        err = "mss kind requires left, top, width, height keys"
        raise ValueError(err) from exc

    return x1, y1, x1 + w, y1 + h


def parse_coords(kind: BBoxKind, coords: BBoxCoordsInput) -> tuple[Number, Number, Number, Number]:
    if kind == BBoxKind.X1Y1X2Y2:
        return _parse_linear(coords, message="x1y1x2y2 kind expects 4 numeric values")

    if kind == BBoxKind.X1Y1WH:
        x1, y1, w, h = _parse_linear(coords, message="x1y1wh kind expects 4 numeric values")
        return x1, y1, x1 + w, y1 + h

    if kind == BBoxKind.X1X2Y1Y2:
        x1, x2, y1, y2 = _parse_linear(coords, message="x1x2y1y2 kind expects 4 numeric values")
        return x1, y1, x2, y2

    if kind == BBoxKind.TL_TR_BR_BL:
        return _parse_free_list(coords)

    if kind == BBoxKind.WINOCR:
        mapping = _require_mapping(coords, message="winocr kind expects a mapping")
        return _parse_winocr(mapping)

    if kind == BBoxKind.MSS:
        mapping = _require_mapping(coords, message="mss kind expects a mapping")
        return _parse_mss(mapping)

    err = f"Unacceptable bbox kind <{kind}>"
    raise TypeError(err)


class BaseBBox:
    def __init__(self, coords: BBoxCoordsInput, kind: BBoxKind) -> None:
        x1, y1, x2, y2 = parse_coords(kind, coords)
        self._set_coords(x1, y1, x2, y2)

    @staticmethod
    def _coerce_coord(value: Number) -> Number:
        return value

    @staticmethod
    def _validate_domain(x1: Number, y1: Number, x2: Number, y2: Number) -> None:
        _ = (x1, y1, x2, y2)

    def _set_coords(self, x1: Number, y1: Number, x2: Number, y2: Number) -> None:
        cx1 = self._coerce_coord(x1)
        cy1 = self._coerce_coord(y1)
        cx2 = self._coerce_coord(x2)
        cy2 = self._coerce_coord(y2)
        self._validate_domain(cx1, cy1, cx2, cy2)
        if not ((cx1 <= cx2) and (cy1 <= cy2)):
            err = (
                f"Invalid coords passed, must be: x1({cx1}) <= x2({cx2}) and y1({cy1}) <= y2({cy2})"
            )
            raise ValueError(err)
        self.x1 = cx1
        self.y1 = cy1
        self.x2 = cx2
        self.y2 = cy2

    def is_valid(self) -> bool:
        self._set_coords(self.x1, self.y1, self.x2, self.y2)
        return True

    def __repr__(self) -> str:
        bbox = f"BBox(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
        return f"<{bbox}>"
