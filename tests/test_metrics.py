import pytest

from bbox_objected import AbsBBox
from bbox_objected.services import metrics


def test_get_iou_extremes() -> None:
    bbox = AbsBBox(0, 0, 10, 10)
    assert metrics.get_IoU(bbox, bbox) == pytest.approx(1.0)

    other = AbsBBox(20, 20, 30, 30)
    assert metrics.get_IoU(bbox, other) == pytest.approx(0.0)


def test_get_cos_between_rejects_zero_vector() -> None:
    bbox = AbsBBox(0, 0, 10, 10)
    with pytest.raises(ValueError, match="zero-length"):
        metrics.get_cos_between(bbox, bbox, bbox.xc, bbox.yc)


def test_non_max_suppression_rejects_thr() -> None:
    with pytest.raises(ValueError, match="thr"):
        metrics.non_max_suppression([], thr=-0.1)

    with pytest.raises(ValueError, match="thr"):
        metrics.non_max_suppression([], thr=1.1)


def test_non_max_suppression_rejects_mixed_inputs() -> None:
    bbox = AbsBBox(0, 0, 10, 10)
    with pytest.raises(TypeError, match="coordinate sequences"):
        metrics.non_max_suppression([bbox, (0, 0, 10, 10)], thr=0.5)


def test_non_max_suppression_rejects_scores_length() -> None:
    boxes = [(0, 0, 10, 10), (1, 1, 9, 9)]
    with pytest.raises(ValueError, match="scores length"):
        metrics.non_max_suppression(boxes, thr=0.5, scores=[0.9])


def test_non_max_suppression_rejects_invalid_coords() -> None:
    boxes = [(True, 0, 1, 2)]
    with pytest.raises(TypeError, match="Invalid coordinate"):
        metrics.non_max_suppression(boxes, thr=0.5)


def test_sort_clockwise_returns_same_length() -> None:
    bbox_1 = AbsBBox(0, 0, 10, 10)
    bbox_2 = AbsBBox(20, 0, 30, 10)

    sorted_boxes = metrics.sort_clockwise([bbox_1, bbox_2], 10, 5)
    assert sorted_boxes == [bbox_1, bbox_2]
