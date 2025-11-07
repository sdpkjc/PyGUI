from __future__ import annotations

from pygui.core.keyboard import Keyboard
from pygui.core.types import Key
from tests.conftest import MockBackend


class TestKeyboard:
    def test_press_release_key_enum(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.press(Key.A)
        assert Key.A in mock_backend._pressed_keys
        keyboard.release(Key.A)
        assert Key.A not in mock_backend._pressed_keys

    def test_press_release_key_string(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.press("b")
        assert "b" in mock_backend._pressed_keys
        keyboard.release("b")
        assert "b" not in mock_backend._pressed_keys

    def test_tap_key(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.tap(Key.ENTER)
        assert Key.ENTER not in mock_backend._pressed_keys

    def test_is_pressed(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        assert not keyboard.is_pressed(Key.SHIFT)
        keyboard.press(Key.SHIFT)
        assert keyboard.is_pressed(Key.SHIFT)
        keyboard.release(Key.SHIFT)
        assert not keyboard.is_pressed(Key.SHIFT)

    def test_type_text(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.type("Hello, World!", interval=0.0)

    def test_type_unicode(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.type("你好世界", interval=0.0)

    def test_hotkey_single_modifier(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.hotkey(Key.CTRL, "c", interval=0.0)
        assert Key.CTRL not in mock_backend._pressed_keys
        assert "c" not in mock_backend._pressed_keys

    def test_hotkey_multiple_modifiers(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        keyboard.hotkey(Key.CTRL, Key.SHIFT, Key.A, interval=0.0)
        assert Key.CTRL not in mock_backend._pressed_keys
        assert Key.SHIFT not in mock_backend._pressed_keys
        assert Key.A not in mock_backend._pressed_keys

    def test_context_manager(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        with keyboard.pressed(Key.SHIFT):
            assert keyboard.is_pressed(Key.SHIFT)
        assert not keyboard.is_pressed(Key.SHIFT)

    def test_layout(self, mock_backend: MockBackend) -> None:
        keyboard = Keyboard()
        layout = keyboard.layout()
        assert layout == "en_US"
