from __future__ import annotations

from typing import Protocol


class ImageLike(Protocol):
    shape: tuple[int, ...]
    ndim: int

    def copy(self) -> ImageLike: ...

    def __getitem__(self, key: object) -> ImageLike: ...
