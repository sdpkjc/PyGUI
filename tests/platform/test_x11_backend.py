"""Unit tests for X11 backend implementation.

These tests verify the X11-specific backend logic and methods.
"""

from __future__ import annotations

import sys

import pytest

# Only run these tests on Linux
pytestmark = pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux/X11 only tests")


class TestX11BackendImport:
    """Test X11 backend can be imported and instantiated."""

    def test_import_x11_backend(self) -> None:
        """Test that X11 backend can be imported."""
        from guiguigui.backend.x11 import X11Backend

        assert X11Backend is not None

    def test_create_x11_backend(self) -> None:
        """Test that X11 backend can be instantiated."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        assert backend is not None

    def test_backend_has_required_methods(self) -> None:
        """Test that backend implements all required abstract methods."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Mouse methods
        assert hasattr(backend, "mouse_position")
        assert hasattr(backend, "mouse_move_to")
        assert hasattr(backend, "mouse_move_rel")
        assert hasattr(backend, "mouse_press")
        assert hasattr(backend, "mouse_release")
        assert hasattr(backend, "mouse_scroll")
        assert hasattr(backend, "mouse_is_pressed")

        # Keyboard methods
        assert hasattr(backend, "key_press")
        assert hasattr(backend, "key_release")
        assert hasattr(backend, "key_is_pressed")
        assert hasattr(backend, "key_type_unicode")
        assert hasattr(backend, "get_keyboard_layout")

        # Display methods
        assert hasattr(backend, "get_displays")
        assert hasattr(backend, "get_primary_display")
        assert hasattr(backend, "get_virtual_screen_rect")

        # Window methods
        assert hasattr(backend, "list_windows")
        assert hasattr(backend, "get_active_window")
        assert hasattr(backend, "get_window_at")
        assert hasattr(backend, "focus_window")
        assert hasattr(backend, "move_window")
        assert hasattr(backend, "resize_window")
        assert hasattr(backend, "set_window_state")
        assert hasattr(backend, "get_window_state")
        assert hasattr(backend, "close_window")
        assert hasattr(backend, "set_window_opacity")
        assert hasattr(backend, "set_window_always_on_top")

        # Clipboard methods
        assert hasattr(backend, "clipboard_get_text")
        assert hasattr(backend, "clipboard_set_text")
        assert hasattr(backend, "clipboard_clear")
        assert hasattr(backend, "clipboard_has_text")

        # Permission check
        assert hasattr(backend, "check_permissions")


class TestX11KeyMapping:
    """Test key code mapping for X11."""

    def test_key_mapping_exists(self) -> None:
        """Test that key mapping dictionary exists."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        # Check that _key_code_map is defined
        assert hasattr(backend, "_key_code_map")
        assert isinstance(backend._key_code_map, dict)

    def test_common_keys_mapped(self) -> None:
        """Test that common keys have mappings."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Test some common keys exist in mapping
        common_keys = [
            "a",
            "return",
            "space",
            "shift",
            "ctrl",
            "escape",
            "delete",
        ]

        for key in common_keys:
            assert key in backend._key_code_map, f"Key {key} should be in key code map"


class TestX11MouseButton:
    """Test mouse button operations for X11."""

    def test_mouse_button_press_release(self) -> None:
        """Test mouse button press and release operations."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # These should not raise exceptions
        # Just test that the methods work
        backend.mouse_press(MouseButton.LEFT)
        backend.mouse_release(MouseButton.LEFT)

    def test_mouse_is_pressed_returns_bool(self) -> None:
        """Test that mouse_is_pressed returns a boolean."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Should return a boolean for all button types
        result_left = backend.mouse_is_pressed(MouseButton.LEFT)
        result_right = backend.mouse_is_pressed(MouseButton.RIGHT)
        result_middle = backend.mouse_is_pressed(MouseButton.MIDDLE)

        assert isinstance(result_left, bool)
        assert isinstance(result_right, bool)
        assert isinstance(result_middle, bool)


class TestX11Permissions:
    """Test permission checking on X11."""

    def test_check_permissions_returns_dict(self) -> None:
        """Test that check_permissions returns a dictionary."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        perms = backend.check_permissions()

        assert isinstance(perms, dict)
        assert "accessibility" in perms
        assert "mouse" in perms
        assert "keyboard" in perms
        assert isinstance(perms["accessibility"], bool)
        assert isinstance(perms["mouse"], bool)


class TestX11Keyboard:
    """Test keyboard operations for X11."""

    def test_key_is_pressed_returns_bool(self) -> None:
        """Test that key_is_pressed returns a boolean."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Should return a boolean for various key types
        result_shift = backend.key_is_pressed(Key.SHIFT)
        result_a = backend.key_is_pressed("a")
        result_space = backend.key_is_pressed(Key.SPACE)

        assert isinstance(result_shift, bool)
        assert isinstance(result_a, bool)
        assert isinstance(result_space, bool)


class TestX11KeyboardLayout:
    """Test keyboard layout detection."""

    def test_get_keyboard_layout_returns_string(self) -> None:
        """Test that get_keyboard_layout returns a string."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        layout = backend.get_keyboard_layout()

        assert isinstance(layout, str)
        assert len(layout) > 0


class TestX11Display:
    """Test display-related methods."""

    def test_get_displays_returns_list(self) -> None:
        """Test that get_displays returns a list."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()

        assert isinstance(displays, list)
        assert len(displays) > 0

    def test_display_info_structure(self) -> None:
        """Test that DisplayInfo has correct structure."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()

        for display in displays:
            assert hasattr(display, "id")
            assert hasattr(display, "name")
            assert hasattr(display, "bounds")
            assert hasattr(display, "scale")
            assert hasattr(display, "is_primary")
            assert display.bounds.width > 0
            assert display.bounds.height > 0
            assert display.scale > 0

    def test_get_primary_display(self) -> None:
        """Test that primary display can be retrieved."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        primary = backend.get_primary_display()

        assert primary is not None
        assert primary.is_primary is True

    def test_virtual_screen_rect(self) -> None:
        """Test virtual screen rect calculation."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        rect = backend.get_virtual_screen_rect()

        assert rect.width > 0
        assert rect.height > 0


class TestX11Window:
    """Test window-related methods."""

    def test_list_windows_returns_list(self) -> None:
        """Test that list_windows returns a list."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        windows = backend.list_windows()

        assert isinstance(windows, list)

    def test_get_active_window(self) -> None:
        """Test getting active window."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        active = backend.get_active_window()

        # Might be None if no windows, but should not raise
        if active:
            assert hasattr(active, "title")
            assert hasattr(active, "handle")

    def test_window_manipulation_methods(self) -> None:
        """Test that window manipulation methods work on X11."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import WindowState

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available for testing")

        handle = windows[0].handle

        # These methods should not raise exceptions on X11
        # Note: May not have visible effect in Xvfb environment, but should execute
        backend.set_window_opacity(handle, 0.8)
        backend.set_window_always_on_top(handle, True)
        backend.set_window_always_on_top(handle, False)

        # Window state operations
        try:
            backend.set_window_state(handle, WindowState.NORMAL)
            state = backend.get_window_state(handle)
            assert isinstance(state, WindowState)
        except Exception:
            # May fail in Xvfb environment without window manager
            pytest.skip("Window state operations require window manager")

    def test_window_get_at_position(self) -> None:
        """Test getting window at position."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Get window at current mouse position
        pos = backend.mouse_position()
        window = backend.get_window_at(pos.x, pos.y)

        # Might be None if no window at that position
        if window:
            assert hasattr(window, "title")
            assert hasattr(window, "handle")


class TestX11EventHooks:
    """Test event hook methods."""

    def test_hook_methods_raise_not_implemented(self) -> None:
        """Test that hook methods raise NotImplementedError."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Hook methods should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            backend.hook_mouse(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.hook_keyboard(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.unhook(None)


class TestX11CoordinateSystem:
    """Test coordinate system handling."""

    def test_mouse_position_in_bounds(self) -> None:
        """Test that mouse position is within screen bounds."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        pos = backend.mouse_position()
        rect = backend.get_virtual_screen_rect()

        # Position should be within virtual screen
        assert pos.x >= rect.x
        assert pos.y >= rect.y
        # Allow some margin for multi-monitor setups
        assert pos.x <= rect.x + rect.width + 1000
        assert pos.y <= rect.y + rect.height + 1000


class TestX11MouseMovement:
    """Test mouse movement operations for X11."""

    def test_mouse_move_to_executes(self) -> None:
        """Test that mouse_move_to executes without error."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Get starting position to restore later
        start_pos = backend.mouse_position()

        # Move to various positions
        backend.mouse_move_to(100, 100)
        backend.mouse_move_to(200, 200, duration=0.1)

        # Restore original position
        backend.mouse_move_to(start_pos.x, start_pos.y)

    def test_mouse_move_to_with_zero_duration(self) -> None:
        """Test instant mouse movement."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Get starting position
        start_pos = backend.mouse_position()

        # Instant move (duration=0.0)
        backend.mouse_move_to(start_pos.x + 10, start_pos.y + 10, duration=0.0)

    def test_mouse_move_rel_executes(self) -> None:
        """Test that mouse_move_rel executes without error."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Relative moves should not raise
        backend.mouse_move_rel(10, 10)
        backend.mouse_move_rel(-10, -10)

    def test_mouse_move_to_negative_coordinates(self) -> None:
        """Test mouse_move_to with negative coordinates."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Negative coordinates should not crash (may be clamped)
        backend.mouse_move_to(-100, -100)

    def test_mouse_move_to_large_coordinates(self) -> None:
        """Test mouse_move_to with very large coordinates."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Large coordinates should not crash (may be clamped by OS)
        backend.mouse_move_to(10000, 10000)


class TestX11MouseScroll:
    """Test mouse scroll operations for X11."""

    def test_mouse_scroll_vertical(self) -> None:
        """Test vertical mouse scroll."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Vertical scroll should not raise
        backend.mouse_scroll(0, 5)  # Scroll up
        backend.mouse_scroll(0, -5)  # Scroll down

    def test_mouse_scroll_horizontal(self) -> None:
        """Test horizontal mouse scroll."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Horizontal scroll should not raise
        backend.mouse_scroll(5, 0)  # Scroll right
        backend.mouse_scroll(-5, 0)  # Scroll left

    def test_mouse_scroll_diagonal(self) -> None:
        """Test diagonal mouse scroll."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Diagonal scroll should not raise
        backend.mouse_scroll(3, 3)

    def test_mouse_scroll_zero(self) -> None:
        """Test mouse scroll with zero values."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Zero scroll should not raise
        backend.mouse_scroll(0, 0)

    def test_mouse_scroll_large_values(self) -> None:
        """Test mouse scroll with large values."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Large scroll values should not crash
        backend.mouse_scroll(100, 100)


class TestX11KeyboardPressRelease:
    """Test keyboard press and release operations for X11."""

    def test_key_press_release_with_key_enum(self) -> None:
        """Test key press and release with Key enum."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Press and release should not raise
        backend.key_press(Key.SHIFT)
        backend.key_release(Key.SHIFT)

        backend.key_press(Key.CTRL)
        backend.key_release(Key.CTRL)

    def test_key_press_release_with_string(self) -> None:
        """Test key press and release with string."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Press and release should not raise
        backend.key_press("a")
        backend.key_release("a")

        backend.key_press("1")
        backend.key_release("1")

    def test_key_press_release_special_keys(self) -> None:
        """Test special keys press and release."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Test various special keys
        special_keys = [
            Key.ENTER,
            Key.TAB,
            Key.ESCAPE,
            Key.SPACE,
            Key.BACKSPACE,
            Key.DELETE,
        ]

        for key in special_keys:
            backend.key_press(key)
            backend.key_release(key)

    def test_key_press_release_function_keys(self) -> None:
        """Test function keys press and release."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Test F1 and F12
        backend.key_press(Key.F1)
        backend.key_release(Key.F1)

        backend.key_press(Key.F12)
        backend.key_release(Key.F12)

    def test_key_press_release_arrow_keys(self) -> None:
        """Test arrow keys press and release."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Test all arrow keys
        backend.key_press(Key.UP)
        backend.key_release(Key.UP)

        backend.key_press(Key.DOWN)
        backend.key_release(Key.DOWN)

        backend.key_press(Key.LEFT)
        backend.key_release(Key.LEFT)

        backend.key_press(Key.RIGHT)
        backend.key_release(Key.RIGHT)


class TestX11KeyboardTyping:
    """Test keyboard typing operations for X11."""

    def test_key_type_unicode_ascii(self) -> None:
        """Test typing ASCII characters."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Should not raise for ASCII
        backend.key_type_unicode("a")
        backend.key_type_unicode("A")
        backend.key_type_unicode("1")
        backend.key_type_unicode("!")

    def test_key_type_unicode_string(self) -> None:
        """Test typing multi-character string."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Should not raise for strings
        backend.key_type_unicode("hello")
        backend.key_type_unicode("Hello World")

    def test_key_type_unicode_unicode(self) -> None:
        """Test typing Unicode characters."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Note: Will raise NotImplementedError, but test that it doesn't crash the backend
        try:
            backend.key_type_unicode("你好")
        except NotImplementedError:
            pass  # Expected for X11

        try:
            backend.key_type_unicode("🌍")
        except NotImplementedError:
            pass  # Expected for X11

    def test_key_type_unicode_special_chars(self) -> None:
        """Test typing special characters."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Should not raise for special chars
        backend.key_type_unicode("@#$%")
        backend.key_type_unicode("\n\t")

    def test_key_type_unicode_empty_string(self) -> None:
        """Test typing empty string."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Empty string should not raise
        backend.key_type_unicode("")
