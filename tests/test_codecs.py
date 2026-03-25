import pytest

from bbox_objected import AbsBBox, RelBBox
from bbox_objected.codecs import coco, easyocr, mss, pascal_voc, winocr


def test_coco_length_validation() -> None:
    with pytest.raises(ValueError, match="COCO expects 4"):
        coco.to_abs_bbox((1, 2, 3))


def test_coco_abs_requires_ints() -> None:
    with pytest.raises(TypeError, match="integer coords"):
        coco.to_abs_bbox((1, 2.0, 3, 4))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_coco_round_trip_abs() -> None:
    bbox = coco.to_abs_bbox((10, 20, 30, 40), text="sample")
    assert bbox.as_tuple() == (10, 20, 40, 60)
    assert bbox.text == "sample"
    assert coco.from_abs_bbox(bbox) == (10, 20, 30, 40)


def test_pascal_voc_abs_validation() -> None:
    with pytest.raises(TypeError, match="integer coords"):
        pascal_voc.to_abs_bbox((1.0, 2, 3, 4))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_pascal_voc_round_trip_rel() -> None:
    bbox = pascal_voc.to_rel_bbox((0.1, 0.2, 0.3, 0.4), text="sample")
    assert isinstance(bbox, RelBBox)
    assert bbox.text == "sample"
    assert pascal_voc.from_rel_bbox(bbox) == pytest.approx((0.1, 0.2, 0.3, 0.4))


def test_easyocr_validation() -> None:
    with pytest.raises(ValueError, match="4 points"):
        easyocr.to_rel_bbox(((0.0, 0.0), (1.0, 1.0), (0.0, 1.0)))

    with pytest.raises(TypeError, match="integer coords"):
        easyocr.to_abs_bbox(((0.1, 0.2), (0.3, 0.2), (0.3, 0.4), (0.1, 0.4)))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_easyocr_round_trip_abs() -> None:
    bbox = easyocr.to_abs_bbox(((1, 2), (3, 2), (3, 4), (1, 4)), text="sample")
    assert isinstance(bbox, AbsBBox)
    assert bbox.text == "sample"
    assert easyocr.from_abs_bbox(bbox)[0] == (1, 2)


def test_winocr_validation() -> None:
    with pytest.raises(ValueError, match="keys"):
        winocr.to_abs_bbox({"x": 1, "y": 2, "width": 3})

    with pytest.raises(TypeError, match="integer coords"):
        winocr.to_abs_bbox({"x": 1, "y": 2, "width": 3, "height": 4.0})  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_mss_validation() -> None:
    with pytest.raises(ValueError, match="keys"):
        mss.to_abs_bbox({"left": 1, "top": 2, "width": 3})

    with pytest.raises(TypeError, match="integer coords"):
        mss.to_abs_bbox({"left": 1, "top": 2, "width": 3, "height": 4.0})  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_mss_round_trip_abs() -> None:
    bbox = mss.to_abs_bbox({"left": 5, "top": 6, "width": 7, "height": 8}, text="sample")
    assert isinstance(bbox, AbsBBox)
    assert bbox.text == "sample"
    assert mss.from_abs_bbox(bbox) == {"left": 5, "top": 6, "width": 7, "height": 8}
