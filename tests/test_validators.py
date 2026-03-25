import pytest

from bbox_objected.domain import validators


def test_validate_order_rejects_inversion() -> None:
    with pytest.raises(ValueError, match="x1"):
        validators.validate_order(2, 0, 1, 1)


def test_validate_abs_rejects_floats() -> None:
    with pytest.raises(TypeError, match="int"):
        validators.validate_abs(1.0, 0, 1, 1)


def test_validate_rel_rejects_ints() -> None:
    with pytest.raises(TypeError, match="float coords"):
        validators.validate_rel(0, 0.1, 0.2, 0.3)


def test_validate_rel_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        validators.validate_rel(0.0, 0.1, 1.1, 0.2)
