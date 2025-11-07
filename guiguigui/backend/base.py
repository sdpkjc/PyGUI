from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from ..core.types import (
    DisplayInfo,
    Key,
    KeyboardEvent,
    MouseButton,
    MouseEvent,
    Point,
    Rect,
    WindowInfo,
    WindowState,
)


class Backend(ABC):
    @abstractmethod
    def mouse_position(self) -> Point:
        pass

    @abstractmethod
    def mouse_move_to(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def mouse_move_rel(self, dx: int, dy: int) -> None:
        pass

    @abstractmethod
    def mouse_press(self, button: MouseButton) -> None:
        pass

    @abstractmethod
    def mouse_release(self, button: MouseButton) -> None:
        pass

    @abstractmethod
    def mouse_scroll(self, dx: int, dy: int) -> None:
        pass

    @abstractmethod
    def mouse_is_pressed(self, button: MouseButton) -> bool:
        pass

    @abstractmethod
    def key_press(self, key: Key | str) -> None:
        pass

    @abstractmethod
    def key_release(self, key: Key | str) -> None:
        pass

    @abstractmethod
    def key_is_pressed(self, key: Key | str) -> bool:
        pass

    @abstractmethod
    def key_type_unicode(self, text: str) -> None:
        pass

    @abstractmethod
    def get_keyboard_layout(self) -> str:
        pass

    @abstractmethod
    def get_displays(self) -> list[DisplayInfo]:
        pass

    @abstractmethod
    def get_primary_display(self) -> DisplayInfo:
        pass

    @abstractmethod
    def get_virtual_screen_rect(self) -> Rect:
        pass

    @abstractmethod
    def list_windows(self, visible_only: bool = True) -> list[WindowInfo]:
        pass

    @abstractmethod
    def get_active_window(self) -> WindowInfo | None:
        pass

    @abstractmethod
    def get_window_at(self, x: int, y: int) -> WindowInfo | None:
        pass

    @abstractmethod
    def focus_window(self, handle: Any) -> None:
        pass

    @abstractmethod
    def move_window(self, handle: Any, x: int, y: int) -> None:
        pass

    @abstractmethod
    def resize_window(self, handle: Any, width: int, height: int) -> None:
        pass

    @abstractmethod
    def set_window_state(self, handle: Any, state: WindowState) -> None:
        pass

    @abstractmethod
    def get_window_state(self, handle: Any) -> WindowState:
        pass

    @abstractmethod
    def close_window(self, handle: Any) -> None:
        pass

    @abstractmethod
    def set_window_opacity(self, handle: Any, opacity: float) -> None:
        pass

    @abstractmethod
    def set_window_always_on_top(self, handle: Any, enabled: bool) -> None:
        pass

    @abstractmethod
    def clipboard_get_text(self) -> str:
        pass

    @abstractmethod
    def clipboard_set_text(self, text: str) -> None:
        pass

    @abstractmethod
    def clipboard_clear(self) -> None:
        pass

    @abstractmethod
    def clipboard_has_text(self) -> bool:
        pass

    def hook_mouse(self, callback: Callable[[MouseEvent], bool]) -> Any:
        raise NotImplementedError("Mouse hook not supported on this platform")

    def hook_keyboard(self, callback: Callable[[KeyboardEvent], bool]) -> Any:
        raise NotImplementedError("Keyboard hook not supported on this platform")

    def unhook(self, hook_handle: Any) -> None:
        raise NotImplementedError("Hook not supported on this platform")

    @abstractmethod
    def check_permissions(self) -> dict[str, bool]:
        pass
