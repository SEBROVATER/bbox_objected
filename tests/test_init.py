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
    assert bbox.x1 == 0.1
    assert bbox.x2 == 0.3
    assert bbox.y1 == 0.2
    assert bbox.y2 == 0.4


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
