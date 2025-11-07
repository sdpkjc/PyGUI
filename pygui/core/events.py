from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..backend import get_backend
from .types import KeyboardEvent, MouseEvent


class Events:
    def __init__(self):
        self._backend = get_backend()
        self._hooks: dict[Any, str] = {}

    def on_mouse(self, callback: Callable[[MouseEvent], bool]) -> Any:
        handle = self._backend.hook_mouse(callback)
        self._hooks[handle] = "mouse"
        return handle

    def on_keyboard(self, callback: Callable[[KeyboardEvent], bool]) -> Any:
        handle = self._backend.hook_keyboard(callback)
        self._hooks[handle] = "keyboard"
        return handle

    def unhook(self, handle: Any) -> None:
        if handle in self._hooks:
            self._backend.unhook(handle)
            del self._hooks[handle]

    def unhook_all(self) -> None:
        for handle in list(self._hooks.keys()):
            self.unhook(handle)


events = Events()
