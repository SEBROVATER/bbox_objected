from ..bbox_img import BBoxImgMixin
from .getter import PyWinAutoBBoxGetter


class PyWinAutoBBox(PyWinAutoBBoxGetter, BBoxImgMixin):
    """Uses PyWinAuto for getting real coords of window during workflow.

    Args:
        window - pywinauto object, must have .rectangle()

    """

    def __init__(self, window, text: str = "", **kwargs) -> None:  # noqa: ANN001
        self.window = window
        self.text = text
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        bbox = self.window.rectangle()
        if text := self.text:
            text = f" - {self.text}"
        return f"<PyWinAutoBBox{bbox}{text}>"
