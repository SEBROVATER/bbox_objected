from typing import TYPE_CHECKING

import pytest

from bbox_objected import AbsBBox, RelBBox


def test_abs_init_correct() -> None:
    bbox = AbsBBox(1, 2, 3, 4)
    assert bbox.as_tuple() == (1, 2, 3, 4)


def test_rel_init_correct() -> None:
    bbox = RelBBox(0.1, 0.2, 0.3, 0.4)
    assert bbox.as_tuple() == pytest.approx((0.1, 0.2, 0.3, 0.4))


def test_abs_init_requires_int() -> None:
    if not TYPE_CHECKING:
        with pytest.raises(TypeError, match="Use only 'int' coords"):
            AbsBBox(1.0, 2.0, 3.0, 4.0)


def test_rel_init_requires_range() -> None:
    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        RelBBox(1.2, 0.1, 0.8, 0.9)


def test_rel_move_preserves_invariant() -> None:
    bbox = RelBBox(0.8, 0.1, 0.9, 0.2)

    with pytest.raises(ValueError, match=r"range \[0, 1\]"):
        bbox.move(0.2, 0.0)


def test_abs_scale_rejects_negative() -> None:
    bbox = AbsBBox(2, 2, 6, 8)

    with pytest.raises(ValueError, match="non-negative"):
        bbox.scale(-2)


def test_replace_and_update_validate_type() -> None:
    abs_bbox = AbsBBox(0, 0, 1, 1)
    rel_bbox = RelBBox(0.1, 0.2, 0.3, 0.4)

    if not TYPE_CHECKING:
        with pytest.raises(TypeError, match="AbsBBox"):
            abs_bbox.replace_from(rel_bbox)

        with pytest.raises(TypeError, match="RelBBox"):
            rel_bbox.update_from(abs_bbox)


def test_conversion_requires_positive_image_size() -> None:
    abs_bbox = AbsBBox(0, 0, 10, 10)
    rel_bbox = RelBBox(0.1, 0.2, 0.3, 0.4)

    with pytest.raises(ValueError, match="must be positive"):
        abs_bbox.as_rel(0, 100)

    with pytest.raises(ValueError, match="must be positive"):
        rel_bbox.as_abs(100, 0)
