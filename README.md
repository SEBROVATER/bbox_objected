# bbox-objected

---

Makes manipulations with bounding boxes easier in Computer Vision projects. With zero dependencies by default.

---

## Installation:

`pip install bbox-objected`

### Optional dependencies:

`pip install numpy`

`pip install opencv-python` or `pip install opencv-contrib-python`

## Examples:
`AbsBBox` is needed to store absolute coordinates (uses `int` type strictly)

```python
from bbox_objected import AbsBBox

bbox = AbsBBox((35, 45, 100, 80), kind="x1y1wh", text="abs_sample")

assert repr(bbox) == "<AbsBBox(x1=35, y1=45, x2=135, y2=125) - abs_sample>"
assert bbox.get_x1y1x2y2() == (35, 45, 135, 125)
```
If you need to store relative coordinates, you can use `RelBBox` (values in range [0., 1.])

```python
from bbox_objected import RelBBox

bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind="x1x2y1y2", text="rel_sample")

assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.5, x2=0.2, y2=0.6) - rel_sample>"
assert bbox.get_tl_tr_br_bl() == ((0.1, 0.5), (0.2, 0.5), (0.2, 0.6), (0.1, 0.6))
```
Conversion between types is available

```python
from bbox_objected import RelBBox

bbox = RelBBox((0.1, 0.2, 0.5, 0.6), kind="x1y1x2y2", text="sample")

assert repr(bbox) == "<RelBBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6) - sample>"
assert (
    repr(bbox.as_abs(1920, 1080))
    == "<AbsBBox(x1=192, y1=216, x2=960, y2=648) - sample>"
)
assert (
    bbox.as_abs(1920, 1080).as_rel(1920, 1080) is not bbox
)
```
There is a bunch of attributes for each bbox

```python
from bbox_objected import RelBBox, AbsBBox

bbox = AbsBBox((40, 40, 60, 60))

assert (bbox.x1, bbox.y1, bbox.x2, bbox.y2) == (40, 40, 60, 60)
assert (bbox.w, bbox.h) == (20, 20)
assert (bbox.tl, bbox.tr, bbox.br, bbox.bl) == ((40, 40), (60, 40), (60, 60), (40, 60))

bbox = AbsBBox((40, 40, 60, 60))

assert (bbox.center, bbox.area) == ((50.0, 50.0), 400)
assert (bbox.xc, bbox.yc) == (50.0, 50.0)
```
Available _**kinds**_ of bboxes:

```python
from bbox_objected.types import BBoxKind

# special format of 'EasyOCR' library
assert BBoxKind.free_list == "tl_tr_br_bl"
assert BBoxKind.tl_tr_br_bl == "tl_tr_br_bl"
# special format of 'EasyOCR' library
assert BBoxKind.horizontal_list == "x1x2y1y2"
assert BBoxKind.x1x2y1y2 == "x1x2y1y2"
# own format of PascalVOC image dataset
assert BBoxKind.pascal_voc == "x1y1x2y2"
assert BBoxKind.x1y1x2y2 == "x1y1x2y2"
# own format of COCO image dataset
assert BBoxKind.coco == "x1y1wh"
assert BBoxKind.x1y1wh == "x1y1wh"
# gets object of '.rectangle()' method of 'PyWinAuto' library
assert BBoxKind.pywinauto == "pywinauto"
# gets special coords format of 'WinOCR' library
assert BBoxKind.winocr == "winocr"
# gets 'monitor' object of library 'mss'
assert BBoxKind.mss == "mss"
```
There is respective `get_` method for each bbox _**kind**_, except `"pywinauto"` and `"winocr"`

Some simple editing of bboxes is also available

```python
from bbox_objected import AbsBBox

bbox = AbsBBox((100, 200, 300, 400))
assert repr(bbox) == "<AbsBBox(x1=100, y1=200, x2=300, y2=400)>"

bbox.zero_basis()
assert repr(bbox) == "<AbsBBox(x1=0, y1=0, x2=200, y2=200)>"

bbox.move_basis(25, 45)
assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=225, y2=245)>"

other_bbox = AbsBBox((200, 300, 400, 500))
assert repr(other_bbox) == "<AbsBBox(x1=200, y1=300, x2=400, y2=500)>"

# chooses coords to get max area, doesn't create new instance
bbox.update_from(other_bbox)
assert repr(bbox) == "<AbsBBox(x1=25, y1=45, x2=400, y2=500)>"

# takes all coords from 'other', doesn't create new instance
bbox.replace_from(other_bbox)
assert repr(bbox) == "<AbsBBox(x1=200, y1=300, x2=400, y2=500)>"
```


## Additional functionality:
Each bbox can be drawn or cropped from image. Can work both with `AbsBBox` and `RelBBox`

```python
import numpy as np
import cv2

from bbox_objected import AbsBBox

bbox = AbsBBox((100, 200, 300, 400))  # 'x1y1x2y2' bbox kind is default

img = np.empty((512, 512, 3), dtype=np.uint8)  # random RGB image

cropped = bbox.crop_from(img)  # 'numpy' must be installed
assert cropped.shape == (200, 200, 3)

bbox.show_on(img, text="sample")  # 'opencv' must be installed
cv2.waitKey(1)
cv2.destroyAllWindows()
```
Also, there are several useful functions. Currently works only with `AbsBBox`.

```python
from bbox_objected import AbsBBox
from bbox_objected.bbox_utils import get_distance, get_IoU, get_cos_between

bbox_1 = AbsBBox((100, 200, 300, 400), kind="x1y1wh")
bbox_2 = AbsBBox((100, 400, 100, 400), kind="horizontal_list")

assert get_distance(bbox_1, bbox_2) == 150.0
# Intersection over Union
assert get_IoU(bbox_1, bbox_2) == 0.4
# angle around center in (450 ,350)
assert get_cos_between(bbox_1, bbox_2, 450, 350) == 0.7592566023652966
```

