from __future__ import annotations

import re
from collections.abc import Callable

from ..backend import get_backend
from .types import Rect, WindowInfo, WindowState


class Window:
    def __init__(self):
        self._backend = get_backend()

    def list(self, visible_only: bool = True) -> list[WindowInfo]:
        return self._backend.list_windows(visible_only)

    def active(self) -> WindowInfo | None:
        return self._backend.get_active_window()

    def find(
        self,
        title: str | None = None,
        class_name: str | None = None,
        pid: int | None = None,
        process_name: str | None = None,
        regex: bool = False,
        predicate: Callable[[WindowInfo], bool] | None = None,
    ) -> WindowInfo | None:
        """Find a window matching the given criteria.

        Returns the first matching window or None if not found.
        """
        windows = self.list(visible_only=True)

        for win in windows:
            if title:
                if regex:
                    if not re.search(title, win.title):
                        continue
                elif title.lower() not in win.title.lower():
                    continue

            if class_name and class_name.lower() not in win.class_name.lower():
                continue

            if pid is not None and win.pid != pid:
                continue

            if process_name and process_name.lower() != win.process_name.lower():
                continue

            if predicate and not predicate(win):
                continue

            return win

        return None

    def at_point(self, x: int, y: int) -> WindowInfo | None:
        return self._backend.get_window_at(x, y)

    # Alias for at_point
    def at(self, x: int, y: int) -> WindowInfo | None:
        """Alias for at_point()"""
        return self.at_point(x, y)

    def focus(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.focus_window(handle)

    def close(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.close_window(handle)

    def position(self, window: WindowInfo | int) -> tuple[int, int]:
        if isinstance(window, WindowInfo):
            return (window.rect.x, window.rect.y)
        windows = self.list(visible_only=False)
        for w in windows:
            if w.handle == window:
                return (w.rect.x, w.rect.y)
        raise ValueError("Window not found")

    def size(self, window: WindowInfo | int) -> tuple[int, int]:
        if isinstance(window, WindowInfo):
            return (window.rect.width, window.rect.height)
        windows = self.list(visible_only=False)
        for w in windows:
            if w.handle == window:
                return (w.rect.width, w.rect.height)
        raise ValueError("Window not found")

    def move(self, window: WindowInfo | int, x: int, y: int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.move_window(handle, x, y)

    def resize(self, window: WindowInfo | int, width: int, height: int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.resize_window(handle, width, height)

    def move_resize(
        self, window: WindowInfo | int, x: int, y: int, width: int, height: int
    ) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.move_window(handle, x, y)
        self._backend.resize_window(handle, width, height)

    def set_rect(self, window: WindowInfo | int, rect: Rect) -> None:
        self.move_resize(window, rect.x, rect.y, rect.width, rect.height)

    def minimize(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.MINIMIZED)

    def maximize(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.MAXIMIZED)

    def restore(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.NORMAL)

    def fullscreen(self, window: WindowInfo | int) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.FULLSCREEN)

    def get_state(self, window: WindowInfo | int) -> WindowState:
        handle = window.handle if isinstance(window, WindowInfo) else window
        return self._backend.get_window_state(handle)

    def set_state(self, window: WindowInfo | int, state: WindowState) -> None:
        """Set window state (normal, minimized, maximized, fullscreen)"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, state)

    def set_opacity(self, window: WindowInfo | int, opacity: float) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_opacity(handle, max(0.0, min(1.0, opacity)))

    def set_always_on_top(self, window: WindowInfo | int, enabled: bool) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_always_on_top(handle, enabled)


window = Window()
