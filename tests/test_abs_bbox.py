import pytest

from bbox_objected import AbsBBox, RelBBox


def test_abs_bbox_rejects_bool() -> None:
    with pytest.raises(TypeError, match="int"):
        AbsBBox(True, 0, 1, 2)


def test_abs_bbox_setters_validate_order() -> None:
    bbox = AbsBBox(0, 0, 10, 10)

    with pytest.raises(ValueError, match="x1"):
        bbox.x1 = 20

    with pytest.raises(ValueError, match="y1"):
        bbox.y1 = 20


def test_abs_bbox_scale_rounds() -> None:
    bbox = AbsBBox(1, 2, 5, 6)
    bbox.scale(0.5)

    assert bbox.as_tuple() == (0, 1, 2, 3)


def test_abs_bbox_as_rel_propagates_text() -> None:
    bbox = AbsBBox(10, 20, 30, 40, text="sample")
    rel = bbox.as_rel(100, 200)

    assert isinstance(rel, RelBBox)
    assert rel.text == "sample"
    assert rel.as_tuple() == pytest.approx((0.1, 0.1, 0.3, 0.2))
