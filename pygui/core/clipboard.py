from __future__ import annotations

from ..backend import get_backend


class Clipboard:
    def __init__(self):
        self._backend = get_backend()

    def get_text(self) -> str:
        return self._backend.clipboard_get_text()

    def set_text(self, text: str) -> None:
        self._backend.clipboard_set_text(text)

    def clear(self) -> None:
        self._backend.clipboard_clear()

    def has_text(self) -> bool:
        return self._backend.clipboard_has_text()


clipboard = Clipboard()
