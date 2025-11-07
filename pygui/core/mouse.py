from __future__ import annotations

import time
from collections.abc import Callable

from ..backend import get_backend
from .types import MouseButton, Point


class Mouse:
    def __init__(self):
        self._backend = get_backend()

    def position(self) -> Point:
        return self._backend.mouse_position()

    def move(
        self, x: int, y: int, duration: float = 0.0, easing: Callable[[float], float] | None = None
    ) -> None:
        if duration <= 0:
            self._backend.mouse_move_to(x, y)
            return

        start = self.position()
        steps = max(int(duration * 60), 2)

        for i in range(steps + 1):
            t = i / steps
            if easing:
                t = easing(t)

            current_x = int(start.x + (x - start.x) * t)
            current_y = int(start.y + (y - start.y) * t)
            self._backend.mouse_move_to(current_x, current_y)
            time.sleep(duration / steps)

    def move_rel(self, dx: int, dy: int, duration: float = 0.0) -> None:
        if duration <= 0:
            self._backend.mouse_move_rel(dx, dy)
        else:
            current = self.position()
            self.move(current.x + dx, current.y + dy, duration)

    def click(
        self, button: MouseButton | str = MouseButton.LEFT, clicks: int = 1, interval: float = 0.1
    ) -> None:
        if isinstance(button, str):
            button = MouseButton(button)

        for i in range(clicks):
            self._backend.mouse_press(button)
            time.sleep(0.02)
            self._backend.mouse_release(button)
            if i < clicks - 1:
                time.sleep(interval)

    def double_click(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        self.click(button, clicks=2, interval=0.1)

    def triple_click(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        self.click(button, clicks=3, interval=0.1)

    def right_click(self) -> None:
        self.click(MouseButton.RIGHT)

    def middle_click(self) -> None:
        self.click(MouseButton.MIDDLE)

    def press(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        if isinstance(button, str):
            button = MouseButton(button)
        self._backend.mouse_press(button)

    def release(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        if isinstance(button, str):
            button = MouseButton(button)
        self._backend.mouse_release(button)

    def is_pressed(self, button: MouseButton | str = MouseButton.LEFT) -> bool:
        if isinstance(button, str):
            button = MouseButton(button)
        return self._backend.mouse_is_pressed(button)

    def drag(
        self, x: int, y: int, button: MouseButton | str = MouseButton.LEFT, duration: float = 0.0
    ) -> None:
        if isinstance(button, str):
            button = MouseButton(button)

        self.press(button)
        time.sleep(0.05)
        self.move(x, y, duration)
        time.sleep(0.05)
        self.release(button)

    def drag_rel(
        self, dx: int, dy: int, button: MouseButton | str = MouseButton.LEFT, duration: float = 0.0
    ) -> None:
        current = self.position()
        self.drag(current.x + dx, current.y + dy, button, duration)

    def scroll(self, dx: int = 0, dy: int = 0) -> None:
        self._backend.mouse_scroll(dx, dy)

    def scroll_up(self, clicks: int = 3) -> None:
        self.scroll(dy=clicks)

    def scroll_down(self, clicks: int = 3) -> None:
        self.scroll(dy=-clicks)

    def scroll_left(self, clicks: int = 3) -> None:
        self.scroll(dx=-clicks)

    def scroll_right(self, clicks: int = 3) -> None:
        self.scroll(dx=clicks)

    def smooth_move(self, x: int, y: int, duration: float = 0.5) -> None:
        def ease_in_out_cubic(t: float) -> float:
            if t < 0.5:
                return 4 * t * t * t
            else:
                return 1 - pow(-2 * t + 2, 3) / 2

        self.move(x, y, duration, easing=ease_in_out_cubic)


mouse = Mouse()
