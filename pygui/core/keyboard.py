from __future__ import annotations

import time

from ..backend import get_backend
from .types import Key


class Keyboard:
    def __init__(self):
        self._backend = get_backend()

    def press(self, key: Key | str) -> None:
        self._backend.key_press(key)

    def release(self, key: Key | str) -> None:
        self._backend.key_release(key)

    def tap(self, key: Key | str, times: int = 1, interval: float = 0.05) -> None:
        for i in range(times):
            self.press(key)
            time.sleep(0.01)
            self.release(key)
            if i < times - 1:
                time.sleep(interval)

    def is_pressed(self, key: Key | str) -> bool:
        return self._backend.key_is_pressed(key)

    def write(self, text: str, interval: float = 0.0) -> None:
        if interval <= 0:
            self._backend.key_type_unicode(text)
        else:
            for char in text:
                self._backend.key_type_unicode(char)
                time.sleep(interval)

    def hotkey(self, *keys: Key | str, interval: float = 0.01) -> None:
        for key in keys:
            self.press(key)
            if interval > 0:
                time.sleep(interval)

        time.sleep(0.02)

        for key in reversed(keys):
            self.release(key)
            if interval > 0:
                time.sleep(interval)

    def press_and_hold(self, key: Key | str, duration: float) -> None:
        self.press(key)
        time.sleep(duration)
        self.release(key)

    def get_modifiers(self) -> set[Key]:
        modifiers = set()
        modifier_keys = [Key.SHIFT, Key.CTRL, Key.ALT, Key.CMD, Key.WIN, Key.SUPER]
        for key in modifier_keys:
            try:
                if self.is_pressed(key):
                    modifiers.add(key)
            except Exception:
                pass
        return modifiers

    def get_layout(self) -> str:
        return self._backend.get_keyboard_layout()


keyboard = Keyboard()
