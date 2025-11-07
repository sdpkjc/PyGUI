from __future__ import annotations

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
        predicate: Callable[[WindowInfo], bool] | None = None,
    ) -> list[WindowInfo]:
        windows = self.list(visible_only=True)
        results: list[WindowInfo] = []

        for win in windows:
            if title and title.lower() not in win.title.lower():
                continue
            if class_name and class_name.lower() not in win.class_name.lower():
                continue
            if pid is not None and win.pid != pid:
                continue
            if predicate and not predicate(win):
                continue
            results.append(win)

        return results

    def at_point(self, x: int, y: int) -> WindowInfo | None:
        return self._backend.get_window_at(x, y)

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

    def set_opacity(self, window: WindowInfo | int, opacity: float) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_opacity(handle, max(0.0, min(1.0, opacity)))

    def set_always_on_top(self, window: WindowInfo | int, enabled: bool) -> None:
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_always_on_top(handle, enabled)


window = Window()
