# bbox-objected

Mutable bounding boxes for computer vision.
Zero required dependencies.

## Contents

- [Install](#install)
- [At A Glance](#at-a-glance)
- [Quickstart](#quickstart)
- [Conversion](#conversion)
- [Geometry And Attributes](#geometry-and-attributes)
- [Editing](#editing)
- [Codecs](#codecs)
- [Adapters](#adapters)
- [Metrics](#metrics)
- [Docs As Tests](#docs-as-tests)

## At A Glance

```text
AbsBBox  <->  RelBBox
   |            |
   |            +-- as_abs(img_w, img_h)
   +-- as_rel(img_w, img_h)

Codecs: coco | pascal_voc | easyocr | winocr | mss
Adapters: numpy crop | opencv draw
Metrics: IoU | distance | angle | NMS | sort_clockwise
```

## Install

Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer):

`uv add bbox-objected`

### Optional dependencies

`numpy` and `opencv` are optional. Install them manually or use extras:

- `uv add "bbox-objected[opencv]"` (opencv + numpy)
- `uv add "bbox-objected[headless]"` (opencv-headless + numpy)
- `uv add "bbox-objected[contrib]"` (opencv-contrib + numpy)
- `uv add "bbox-objected[contrib-headless]"` (opencv-contrib-headless + numpy)

> Note: different `opencv` variants are mutually incompatible.

## Quickstart

`AbsBBox` stores absolute integer coordinates:

```python
from bbox_objected import AbsBBox

# Create a bbox with absolute coordinates.
bbox = AbsBBox(35, 45, 135, 125, text="abs_sample")

assert repr(bbox) == "<AbsBBox(x1=35, y1=45, x2=135, y2=125) - abs_sample>"
assert bbox.as_tuple() == (35, 45, 135, 125)
```

`RelBBox` stores relative coordinates in `[0.0, 1.0]`:

```python
from bbox_objected import RelBBox

# Create a bbox with relative coordinates.
bbox = RelBBox(0.1, 0.5, 0.2, 0.6, text="rel_sample")

assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.5, x2=0.2, y2=0.6) - rel_sample>"
assert bbox.tl == (0.1, 0.5)
```

## Conversion

Convert between absolute and relative forms when image size is known:

```python
from bbox_objected import RelBBox

# Convert between coordinate systems.
bbox = RelBBox(0.1, 0.2, 0.5, 0.6, text="sample")

assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6) - sample>"
assert repr(bbox.as_abs(1920, 1080)) == "<AbsBBox(x1=192, y1=216, x2=960, y2=648) - sample>"
assert bbox.as_abs(1920, 1080).as_rel(1920, 1080) is not bbox
```

## Geometry And Attributes

Each bbox exposes geometry helpers and derived attributes.

Need mutation? Jump to [Editing](#editing).

```python
from bbox_objected import AbsBBox

# Access coordinate and geometry helpers.
bbox = AbsBBox(40, 40, 60, 60)

assert (bbox.x1, bbox.y1, bbox.x2, bbox.y2) == (40, 40, 60, 60)
assert (bbox.w, bbox.h) == (20, 20)
assert (bbox.tl, bbox.tr, bbox.br, bbox.bl) == ((40, 40), (60, 40), (60, 60), (40, 60))
assert (bbox.center, bbox.area) == ((50.0, 50.0), 400)
assert (bbox.xc, bbox.yc) == (50.0, 50.0)
```

## Editing

Mutate existing boxes in-place for long-lived objects:

Need format conversions? See [Codecs](#codecs).

```python
from bbox_objected import AbsBBox

# Edit coords in-place to avoid new objects.
bbox = AbsBBox(100, 200, 300, 400)
assert repr(bbox) == "<AbsBBox(x1=100, y1=200, x2=300, y2=400)>"

bbox.zero_basis()
assert repr(bbox) == "<AbsBBox(x1=0, y1=0, x2=200, y2=200)>"

bbox.move(25, 45)
assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=225, y2=245)>"

other_bbox = AbsBBox(200, 300, 400, 500)

# Expands current box to cover both.
bbox.update_from(other_bbox)
assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=400, y2=500)>"

# Replaces current coords with another box.
bbox.replace_from(other_bbox)
assert repr(bbox) == "<AbsBBox(x1=200, y1=300, x2=400, y2=500)>"
```

## Codecs

Use codecs to translate between bbox formats:

Want to crop or draw on images? See [Adapters](#adapters).

```python
from bbox_objected import AbsBBox
from bbox_objected.codecs import coco, easyocr, mss, pascal_voc, winocr

# COCO: x, y, w, h
assert coco.from_abs_bbox(AbsBBox(10, 20, 30, 40)) == (10, 20, 20, 20)

# Pascal VOC: x1, y1, x2, y2
assert pascal_voc.from_abs_bbox(AbsBBox(10, 20, 30, 40)) == (10, 20, 30, 40)

# EasyOCR: tl, tr, br, bl
assert easyocr.from_abs_bbox(AbsBBox(10, 20, 30, 40))[0] == (10, 20)

# WinOCR: mapping
assert winocr.from_abs_bbox(AbsBBox(10, 20, 30, 40))["width"] == 20

# MSS: mapping
assert mss.from_abs_bbox(AbsBBox(10, 20, 30, 40))["height"] == 20
```

## Adapters

Crop using the numpy adapter (requires `numpy`):

```python
import numpy as np

from bbox_objected import AbsBBox
from bbox_objected.adapters import crop_from_image

# Crop using numpy-backed images.
bbox = AbsBBox(100, 200, 300, 400)
img = np.empty((512, 512, 3), dtype=np.uint8)

cropped = crop_from_image(bbox, img)
assert cropped.shape == (200, 200, 3)
```

Draw using the OpenCV adapter (requires `opencv-python` with GUI support):

```python notest
import cv2
import numpy as np

from bbox_objected import AbsBBox
from bbox_objected.adapters import show_on_image

# Requires a GUI-capable OpenCV build.
bbox = AbsBBox(100, 200, 300, 400)
img = np.empty((512, 512, 3), dtype=np.uint8)

show_on_image(bbox, img, text="sample")
cv2.waitKey(1)
cv2.destroyAllWindows()
```

## Metrics

Compute distance, overlap, and angular relations on absolute boxes:

```python
import pytest

from bbox_objected import get_cos_between, get_distance, get_IoU, sort_clockwise
from bbox_objected.codecs import coco, pascal_voc

bbox_1 = coco.to_abs_bbox((100, 200, 300, 400))
bbox_2 = pascal_voc.to_abs_bbox((100, 400, 200, 800))

assert get_distance(bbox_1, bbox_2) == pytest.approx(223.60679774997897)
assert get_IoU(bbox_1, bbox_2) == pytest.approx(0.14285714285714285)
assert get_cos_between(bbox_1, bbox_2, 450, 350) == pytest.approx(0.9005516363645784)

sorted_boxes = sort_clockwise([bbox_1, bbox_2], 450, 350)
assert len(sorted_boxes) == 2
```

Non-max suppression works with tuples and optional scores:

```python
from bbox_objected import non_max_suppression

# Picks indices of boxes with higher scores and low overlap.
boxes = [(10, 10, 20, 20), (11, 11, 19, 19), (50, 50, 70, 70)]
picks = non_max_suppression(boxes, thr=0.5, scores=[0.4, 0.9, 0.8])

assert picks == [1, 2]
```

EasyOCR quad conversion example:

```python
from bbox_objected.codecs import easyocr

bbox = easyocr.to_abs_bbox(((10, 20), (30, 20), (30, 40), (10, 40)))
assert bbox.as_tuple() == (10, 20, 30, 40)
```

## Docs As Tests

README examples are executed as tests via `pytest-markdown-docs`.

- Run locally: `uv run pytest`
- The pytest config enables `--markdown-docs` by default.
