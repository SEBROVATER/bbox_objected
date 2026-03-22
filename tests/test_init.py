import pytest

from bbox_objected import AbsBBox, RelBBox


def test_abs_init_correct() -> None:
    bbox = AbsBBox((1, 2, 3, 4))
    assert bbox.get_x1y1x2y2() == (1, 2, 3, 4)


def test_rel_init_correct() -> None:
    bbox = RelBBox((0.1, 0.2, 0.3, 0.4))
    assert bbox.get_x1y1x2y2() == pytest.approx((0.1, 0.2, 0.3, 0.4))


def test_abs_init_requires_int() -> None:
    with pytest.raises(TypeError, match="Use only 'int' coords"):
        AbsBBox((1.0, 2.0, 3.0, 4.0))


def test_rel_init_requires_range() -> None:
    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        RelBBox((1.2, 0.1, 0.8, 0.9))


def test_rel_move_basis_preserves_invariant() -> None:
    bbox = RelBBox((0.8, 0.1, 0.9, 0.2))

    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        bbox.move_basis(0.2, 0.0)


def test_abs_divide_rejects_non_positive() -> None:
    bbox = AbsBBox((2, 2, 6, 8))

    with pytest.raises(ValueError, match="positive"):
        bbox.divide_by(0)

    with pytest.raises(ValueError, match="positive"):
        bbox.divide_by(-2)


def test_replace_and_update_validate_type() -> None:
    abs_bbox = AbsBBox((0, 0, 1, 1))
    rel_bbox = RelBBox((0.1, 0.2, 0.3, 0.4))

    with pytest.raises(TypeError, match="same bbox class"):
        abs_bbox.replace_from(rel_bbox)

    with pytest.raises(TypeError, match="same bbox class"):
        rel_bbox.update_from(abs_bbox)


def test_conversion_requires_positive_image_size() -> None:
    abs_bbox = AbsBBox((0, 0, 10, 10))
    rel_bbox = RelBBox((0.1, 0.2, 0.3, 0.4))

    with pytest.raises(ValueError, match="must be positive"):
        abs_bbox.as_rel(0, 100)

    with pytest.raises(ValueError, match="must be positive"):
        rel_bbox.as_abs(100, 0)
