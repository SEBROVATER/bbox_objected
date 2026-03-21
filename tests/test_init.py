from decimal import Decimal

import pytest

from bbox_objected import AbsBBox, RelBBox


def test_abs_init_correct():
    bbox = AbsBBox((1, 2, 3, 4))
    assert bbox.x1 == 1
    assert bbox.x2 == 3
    assert bbox.y1 == 2
    assert bbox.y2 == 4


def test_rel_init_correct():
    bbox = RelBBox((0.1, 0.2, 0.3, 0.4))
    assert bbox.x1 == pytest.approx(0.1)
    assert bbox.x2 == pytest.approx(0.3)
    assert bbox.y1 == pytest.approx(0.2)
    assert bbox.y2 == pytest.approx(0.4)


def test_rel_init_decimal_correct():
    bbox = RelBBox((Decimal("0.1"), Decimal("0.2"), Decimal("0.3"), Decimal("0.4")))
    assert bbox.x1 == Decimal("0.1")
    assert bbox.x2 == Decimal("0.3")
    assert bbox.y1 == Decimal("0.2")
    assert bbox.y2 == Decimal("0.4")


def test_abs_init_incorrect():
    with pytest.raises(ValueError, match="Invalid coords"):
        AbsBBox((4, 3, 2, 1))


def test_abs_init_float():
    with pytest.raises(TypeError, match="Invalid coords"):
        AbsBBox((4.0, 3.0, 2.0, 1.0))


def test_rel_init_incorrect():
    with pytest.raises(ValueError, match="Invalid coords"):
        RelBBox((0.4, 0.3, 0.2, 0.1))


def test_rel_init_oob():
    with pytest.raises(ValueError, match="Invalid coords"):
        RelBBox((1.4, -0.3, 0.2, 0.1))


def test_rel_move_basis_requires_same_type() -> None:
    bbox = RelBBox((0.1, 0.2, 0.3, 0.4))

    with pytest.raises(TypeError, match="same numeric type"):
        bbox.move_basis(1, 1)


def test_rel_multiply_divide_keep_compatible_type() -> None:
    bbox = RelBBox((Decimal("0.1"), Decimal("0.2"), Decimal("0.3"), Decimal("0.4")))
    bbox.multiply_by(2)
    assert bbox.x1 == Decimal("0.2")
    assert bbox.y2 == Decimal("0.8")

    bbox.divide_by(4.0)
    assert bbox.x1 == Decimal("0.05")
    assert bbox.y2 == Decimal("0.2")


def test_rel_multiply_clamps_and_rejects_negative() -> None:
    bbox = RelBBox((0.7, 0.8, 0.9, 1.0))
    bbox.multiply_by(2.0)
    assert bbox.x1 == pytest.approx(1.0)
    assert bbox.y2 == pytest.approx(1.0)

    with pytest.raises(ValueError, match="non-negative"):
        bbox.multiply_by(-0.5)


def test_rel_divide_clamps_and_rejects_non_positive() -> None:
    bbox = RelBBox((0.1, 0.2, 0.3, 0.4))
    bbox.divide_by(0.1)
    assert bbox.x1 == pytest.approx(1.0)
    assert bbox.y2 == pytest.approx(1.0)

    with pytest.raises(ValueError, match="positive"):
        bbox.divide_by(0.0)
    with pytest.raises(ValueError, match="positive"):
        bbox.divide_by(-2.0)
