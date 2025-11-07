from __future__ import annotations

import time

from pygui.core.mouse import Mouse
from pygui.core.types import MouseButton, Point
from tests.conftest import MockBackend


class TestMouse:
    def test_position(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mock_backend._mouse_position = Point(100, 200)
        assert mouse.position() == Point(100, 200)

    def test_move_to(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.move(500, 600)
        assert mock_backend._mouse_position == Point(500, 600)

    def test_move_relative(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mock_backend._mouse_position = Point(100, 100)
        mouse.move_rel(50, 75)
        assert mock_backend._mouse_position == Point(150, 175)

    def test_move_with_duration(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        start_time = time.time()
        mouse.move(1000, 1000, duration=0.1)
        elapsed = time.time() - start_time
        assert elapsed >= 0.1
        assert mock_backend._mouse_position == Point(1000, 1000)

    def test_click_left(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.click(MouseButton.LEFT)
        assert MouseButton.LEFT not in mock_backend._pressed_buttons

    def test_click_right(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.click(MouseButton.RIGHT)
        assert MouseButton.RIGHT not in mock_backend._pressed_buttons

    def test_double_click(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.double_click(MouseButton.LEFT)
        assert MouseButton.LEFT not in mock_backend._pressed_buttons

    def test_press_release(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.press(MouseButton.LEFT)
        assert mock_backend._pressed_buttons == {MouseButton.LEFT}
        mouse.release(MouseButton.LEFT)
        assert MouseButton.LEFT not in mock_backend._pressed_buttons

    def test_is_pressed(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        assert not mouse.is_pressed(MouseButton.LEFT)
        mouse.press(MouseButton.LEFT)
        assert mouse.is_pressed(MouseButton.LEFT)
        mouse.release(MouseButton.LEFT)
        assert not mouse.is_pressed(MouseButton.LEFT)

    def test_scroll(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mouse.scroll(0, 5)

    def test_drag(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mock_backend._mouse_position = Point(100, 100)
        mouse.drag(200, 200, button=MouseButton.LEFT, duration=0.1)
        assert mock_backend._mouse_position == Point(200, 200)
        assert MouseButton.LEFT not in mock_backend._pressed_buttons

    def test_context_manager(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        with mouse.pressed(MouseButton.RIGHT):
            assert mouse.is_pressed(MouseButton.RIGHT)
        assert not mouse.is_pressed(MouseButton.RIGHT)
