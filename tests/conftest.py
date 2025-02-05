from collections.abc import Generator
from types import ModuleType
from unittest import mock

import pytest


@pytest.fixture
def numpy_uninstalled() -> Generator[None, None, None]:
    import builtins

    real_import = builtins.__import__

    def import_mock(name: str, *args) -> ModuleType:
        if name == "numpy":
            err = "Mock uninstalled 'numpy'"
            raise ImportError(err)
        return real_import(name, *args)

    with mock.patch("builtins.__import__", import_mock):
        yield
