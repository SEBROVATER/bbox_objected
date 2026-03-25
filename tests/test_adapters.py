import importlib

import pytest

from bbox_objected import AbsBBox, RelBBox
from bbox_objected.adapters import crop_from_image, show_on_image


def test_crop_from_image_abs_bbox() -> None:
    np = pytest.importorskip("numpy")

    bbox = AbsBBox(10, 20, 30, 50)
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    cropped = crop_from_image(bbox, img)
    assert cropped.shape == (30, 20, 3)


def test_crop_from_image_rel_bbox() -> None:
    np = pytest.importorskip("numpy")

    bbox = RelBBox(0.1, 0.2, 0.3, 0.5)
    img = np.zeros((100, 200, 3), dtype=np.uint8)

    cropped = crop_from_image(bbox, img)
    assert cropped.shape == (30, 40, 3)


def test_show_on_image_requires_opencv(monkeypatch: pytest.MonkeyPatch) -> None:
    np = pytest.importorskip("numpy")

    def _raise(_: str) -> None:
        raise ModuleNotFoundError

    monkeypatch.setattr(importlib, "import_module", _raise)

    fake_img = np.zeros((10, 10, 3), dtype=np.uint8)
    with pytest.raises(NotImplementedError, match="OpenCV"):
        show_on_image(AbsBBox(0, 0, 1, 1), fake_img)
