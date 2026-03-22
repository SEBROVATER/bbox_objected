import pytest

from bbox_objected import (
    AbsBBox,
    RelBBox,
    crop_from_image,
    get_cos_between,
    get_distance,
    get_IoU,
    non_max_suppression,
    sort_clockwise,
)
from bbox_objected.annotations import BBoxKind


def test_abs_bbox() -> None:
    bbox = AbsBBox((35, 45, 100, 80), kind=BBoxKind.X1Y1WH, text="abs_sample")

    assert repr(bbox) == "<AbsBBox(x1=35, y1=45, x2=135, y2=125) - abs_sample>"
    assert bbox.get_x1y1x2y2() == (35, 45, 135, 125)


def test_rel_bbox() -> None:
    bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind=BBoxKind.X1X2Y1Y2, text="rel_sample")

    assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.5, x2=0.2, y2=0.6) - rel_sample>"
    assert bbox.get_tl_tr_br_bl() == ((0.1, 0.5), (0.2, 0.5), (0.2, 0.6), (0.1, 0.6))


def test_conversion() -> None:
    bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind=BBoxKind.X1Y1X2Y2, text="sample")

    assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6) - sample>"
    assert repr(bbox.as_abs(1920, 1080)) == "<AbsBBox(x1=192, y1=216, x2=960, y2=648) - sample>"
    assert bbox.as_abs(1920, 1080).as_rel(1920, 1080) is not bbox


def test_attributes() -> None:
    bbox = AbsBBox((40, 40, 60, 60))

    assert (bbox.x1, bbox.y1, bbox.x2, bbox.y2) == (40, 40, 60, 60)
    assert (bbox.w, bbox.h) == (20, 20)
    assert (bbox.tl, bbox.tr, bbox.br, bbox.bl) == ((40, 40), (60, 40), (60, 60), (40, 60))
    assert (bbox.center, bbox.area) == ((50.0, 50.0), 400)
    assert (bbox.xc, bbox.yc) == (50.0, 50.0)


def test_kinds() -> None:
    assert str(BBoxKind.TL_TR_BR_BL) == "tl_tr_br_bl"
    assert str(BBoxKind.X1X2Y1Y2) == "x1x2y1y2"
    assert str(BBoxKind.X1Y1X2Y2) == "x1y1x2y2"
    assert str(BBoxKind.X1Y1WH) == "x1y1wh"
    assert str(BBoxKind.WINOCR) == "winocr"
    assert str(BBoxKind.MSS) == "mss"


def test_editors() -> None:
    bbox = AbsBBox((100, 200, 300, 400))
    assert repr(bbox) == "<AbsBBox(x1=100, y1=200, x2=300, y2=400)>"

    bbox.zero_basis()
    assert repr(bbox) == "<AbsBBox(x1=0, y1=0, x2=200, y2=200)>"

    bbox.move_basis(25, 45)
    assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=225, y2=245)>"

    other_bbox = AbsBBox((200, 300, 400, 500))
    bbox.update_from(other_bbox)
    assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=400, y2=500)>"

    bbox.replace_from(other_bbox)
    assert repr(bbox) == "<AbsBBox(x1=200, y1=300, x2=400, y2=500)>"


def test_crop_from_image() -> None:
    np = pytest.importorskip("numpy")

    bbox = AbsBBox((100, 200, 300, 400))
    img = np.empty((512, 512, 3), dtype=np.uint8)

    cropped = crop_from_image(bbox, img)
    assert cropped.shape == (200, 200, 3)


def test_bbox_utils() -> None:
    bbox_1 = AbsBBox((100, 200, 300, 400), kind=BBoxKind.X1Y1WH)
    bbox_2 = AbsBBox((100, 400, 100, 400), kind=BBoxKind.X1X2Y1Y2)

    assert get_distance(bbox_1, bbox_2) == pytest.approx(150.0)
    assert get_IoU(bbox_1, bbox_2) == pytest.approx(0.4)
    assert get_cos_between(bbox_1, bbox_2, 450, 350) == pytest.approx(0.7592566023652966)

    sorted_boxes = sort_clockwise([bbox_1, bbox_2], 450, 350)
    assert len(sorted_boxes) == 2


def test_non_max_suppression_with_scores() -> None:
    boxes = [(10, 10, 20, 20), (11, 11, 19, 19), (50, 50, 70, 70)]
    picks = non_max_suppression(boxes, thr=0.5, scores=[0.4, 0.9, 0.8])

    assert picks == [1, 2]
