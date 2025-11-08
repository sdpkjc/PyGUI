from __future__ import annotations

import time

import pytest

from guiguigui import display, mouse
from guiguigui.core.types import MouseButton, Point


@pytest.mark.integration
class TestMouseOperations:
    def test_mouse_position(self) -> None:
        pos = mouse.position()
        assert isinstance(pos, Point)
        assert isinstance(pos.x, int)
        assert isinstance(pos.y, int)

    def test_mouse_move_absolute(self) -> None:
        initial_pos = mouse.position()
        target_x, target_y = 500, 500

        mouse.move(target_x, target_y)
        time.sleep(0.1)

        new_pos = mouse.position()
        assert new_pos.x == target_x
        assert new_pos.y == target_y

        mouse.move(initial_pos.x, initial_pos.y)

    def test_mouse_move_relative(self) -> None:
        initial_pos = mouse.position()

        mouse.move_rel(100, 50)
        time.sleep(0.1)

        new_pos = mouse.position()
        assert new_pos.x == initial_pos.x + 100
        assert new_pos.y == initial_pos.y + 50

        mouse.move(initial_pos.x, initial_pos.y)

    def test_mouse_move_with_duration(self) -> None:
        initial_pos = mouse.position()
        target_x, target_y = 800, 600
        duration = 0.5

        start_time = time.time()
        mouse.move(target_x, target_y, duration=duration)
        elapsed = time.time() - start_time

        assert elapsed >= duration
        assert mouse.position() == Point(target_x, target_y)

        mouse.move(initial_pos.x, initial_pos.y)

    def test_mouse_click(self) -> None:
        mouse.click()
        time.sleep(0.1)

    def test_mouse_double_click(self) -> None:
        mouse.double_click()
        time.sleep(0.1)

    def test_mouse_press_release(self) -> None:
        mouse.press(MouseButton.LEFT)
        time.sleep(0.05)
        assert mouse.is_pressed(MouseButton.LEFT)
        mouse.release(MouseButton.LEFT)
        time.sleep(0.05)
        assert not mouse.is_pressed(MouseButton.LEFT)

    def test_mouse_scroll(self) -> None:
        mouse.scroll(0, 5)
        time.sleep(0.1)
        mouse.scroll(0, -5)
        time.sleep(0.1)

    def test_mouse_drag(self) -> None:
        initial_pos = mouse.position()
        target_x, target_y = initial_pos.x + 200, initial_pos.y + 100

        mouse.drag(target_x, target_y, duration=0.3)
        time.sleep(0.1)

        final_pos = mouse.position()
        assert abs(final_pos.x - target_x) <= 5
        assert abs(final_pos.y - target_y) <= 5

        mouse.move(initial_pos.x, initial_pos.y)

    def test_mouse_within_screen_bounds(self) -> None:
        virtual_rect = display.virtual_screen_rect()

        mouse.move(virtual_rect.x + 100, virtual_rect.y + 100)
        pos = mouse.position()

        assert virtual_rect.left <= pos.x <= virtual_rect.right
        assert virtual_rect.top <= pos.y <= virtual_rect.bottom
