import pytest

from bbox_objected import AbsBBox, RelBBox


def test_rel_bbox_coerces_ints() -> None:
    bbox = RelBBox(0, 0, 1, 1)
    assert bbox.as_tuple() == pytest.approx((0.0, 0.0, 1.0, 1.0))


def test_rel_bbox_rejects_inverted_order() -> None:
    with pytest.raises(ValueError, match="x1"):
        RelBBox(0.6, 0.1, 0.5, 0.2)


def test_rel_bbox_setter_rejects_range() -> None:
    bbox = RelBBox(0.1, 0.1, 0.2, 0.2)

    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        bbox.x1 = -0.1


def test_rel_bbox_as_abs_rounding_and_text() -> None:
    bbox = RelBBox(0.1, 0.25, 0.3, 0.75, text="sample")
    abs_bbox = bbox.as_abs(10, 20)

    assert isinstance(abs_bbox, AbsBBox)
    assert abs_bbox.text == "sample"
    assert abs_bbox.as_tuple() == (1, 5, 3, 15)
