from __future__ import annotations

from typing import Any

import pytest

from pygui.backend.base import Backend
from pygui.core.types import (
    DisplayInfo,
    Key,
    MouseButton,
    Point,
    Rect,
    Size,
    WindowInfo,
    WindowState,
)


class MockBackend(Backend):
    def __init__(self) -> None:
        self._mouse_position = Point(0, 0)
        self._pressed_buttons: set[MouseButton] = set()
        self._pressed_keys: set[Key | str] = set()
        self._clipboard_text = ""
        self._windows: list[WindowInfo] = []
        self._displays: list[DisplayInfo] = []
        self._active_window: WindowInfo | None = None

    def mouse_position(self) -> Point:
        return self._mouse_position

    def mouse_move_to(self, x: int, y: int) -> None:
        self._mouse_position = Point(x, y)

    def mouse_move_rel(self, dx: int, dy: int) -> None:
        self._mouse_position = Point(self._mouse_position.x + dx, self._mouse_position.y + dy)

    def mouse_press(self, button: MouseButton) -> None:
        self._pressed_buttons.add(button)

    def mouse_release(self, button: MouseButton) -> None:
        self._pressed_buttons.discard(button)

    def mouse_scroll(self, dx: int, dy: int) -> None:
        pass

    def mouse_is_pressed(self, button: MouseButton) -> bool:
        return button in self._pressed_buttons

    def key_press(self, key: Key | str) -> None:
        self._pressed_keys.add(key)

    def key_release(self, key: Key | str) -> None:
        self._pressed_keys.discard(key)

    def key_is_pressed(self, key: Key | str) -> bool:
        return key in self._pressed_keys

    def key_type_unicode(self, text: str) -> None:
        pass

    def get_keyboard_layout(self) -> str:
        return "en_US"

    def get_displays(self) -> list[DisplayInfo]:
        if not self._displays:
            self._displays = [
                DisplayInfo(
                    id="display0",
                    name="Main Display",
                    bounds=Rect(0, 0, 1920, 1080),
                    work_area=Rect(0, 0, 1920, 1040),
                    scale=1.0,
                    physical_size=Size(1920, 1080),
                    refresh_rate=60.0,
                    rotation=0,
                    is_primary=True,
                ),
                DisplayInfo(
                    id="display1",
                    name="Secondary Display",
                    bounds=Rect(1920, 0, 1920, 1080),
                    work_area=Rect(1920, 0, 1920, 1040),
                    scale=2.0,
                    physical_size=Size(3840, 2160),
                    refresh_rate=60.0,
                    rotation=0,
                    is_primary=False,
                ),
            ]
        return self._displays

    def get_primary_display(self) -> DisplayInfo:
        displays = self.get_displays()
        for display in displays:
            if display.is_primary:
                return display
        return displays[0]

    def get_virtual_screen_rect(self) -> Rect:
        displays = self.get_displays()
        if not displays:
            return Rect(0, 0, 0, 0)

        min_x = min(d.bounds.x for d in displays)
        min_y = min(d.bounds.y for d in displays)
        max_x = max(d.bounds.x + d.bounds.width for d in displays)
        max_y = max(d.bounds.y + d.bounds.height for d in displays)

        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def list_windows(self, visible_only: bool = True) -> list[WindowInfo]:
        if visible_only:
            return [w for w in self._windows if w.is_visible]
        return self._windows

    def get_active_window(self) -> WindowInfo | None:
        return self._active_window

    def get_window_at(self, x: int, y: int) -> WindowInfo | None:
        point = Point(x, y)
        for window in self._windows:
            if window.rect.contains(point):
                return window
        return None

    def focus_window(self, handle: Any) -> None:
        for window in self._windows:
            if window.handle == handle:
                self._active_window = window
                break

    def move_window(self, handle: Any, x: int, y: int) -> None:
        for window in self._windows:
            if window.handle == handle:
                window.rect.x = x
                window.rect.y = y
                break

    def resize_window(self, handle: Any, width: int, height: int) -> None:
        for window in self._windows:
            if window.handle == handle:
                window.rect.width = width
                window.rect.height = height
                break

    def set_window_state(self, handle: Any, state: WindowState) -> None:
        for window in self._windows:
            if window.handle == handle:
                window.state = state
                break

    def get_window_state(self, handle: Any) -> WindowState:
        for window in self._windows:
            if window.handle == handle:
                return window.state
        return WindowState.NORMAL

    def close_window(self, handle: Any) -> None:
        self._windows = [w for w in self._windows if w.handle != handle]

    def set_window_opacity(self, handle: Any, opacity: float) -> None:
        for window in self._windows:
            if window.handle == handle:
                window.opacity = opacity
                break

    def set_window_always_on_top(self, handle: Any, enabled: bool) -> None:
        for window in self._windows:
            if window.handle == handle:
                window.is_always_on_top = enabled
                break

    def clipboard_get_text(self) -> str:
        return self._clipboard_text

    def clipboard_set_text(self, text: str) -> None:
        self._clipboard_text = text

    def clipboard_clear(self) -> None:
        self._clipboard_text = ""

    def clipboard_has_text(self) -> bool:
        return bool(self._clipboard_text)

    def check_permissions(self) -> dict[str, bool]:
        return {
            "accessibility": True,
            "screen_recording": True,
        }


@pytest.fixture
def mock_backend(monkeypatch: pytest.MonkeyPatch) -> MockBackend:
    backend = MockBackend()
    monkeypatch.setattr("pygui.backend.get_backend", lambda: backend)
    return backend


@pytest.fixture
def sample_window() -> WindowInfo:
    return WindowInfo(
        handle=1,
        title="Test Window",
        class_name="TestClass",
        pid=1234,
        process_name="test_process",
        rect=Rect(100, 100, 800, 600),
        client_rect=Rect(100, 100, 800, 600),
        state=WindowState.NORMAL,
        is_visible=True,
        is_active=False,
        is_always_on_top=False,
        opacity=1.0,
    )
