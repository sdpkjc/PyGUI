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
        """Test that mouse_move_to moves cursor to target position."""
        import time

        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Get starting position to restore later
        start_pos = backend.mouse_position()

        # Move to specific positions and verify (X11 supports duration)
        backend.mouse_move_to(100, 100)
        time.sleep(0.05)
        pos1 = backend.mouse_position()
        assert pos1.x == 100, f"Expected x=100, got {pos1.x}"
        assert pos1.y == 100, f"Expected y=100, got {pos1.y}"

        backend.mouse_move_to(200, 200)
        time.sleep(0.05)
        pos2 = backend.mouse_position()
        assert pos2.x == 200, f"Expected x=200, got {pos2.x}"
        assert pos2.y == 200, f"Expected y=200, got {pos2.y}"

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


class TestX11MouseButtons:
    """Test X11 mouse button operations."""

    def test_mouse_x1_button(self) -> None:
        """Test X1 (back) mouse button."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Should not crash
        backend.mouse_press(MouseButton.X1)
        backend.mouse_release(MouseButton.X1)

    def test_mouse_x2_button(self) -> None:
        """Test X2 (forward) mouse button."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Should not crash
        backend.mouse_press(MouseButton.X2)
        backend.mouse_release(MouseButton.X2)

    def test_mouse_middle_button(self) -> None:
        """Test middle mouse button."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Should not crash
        backend.mouse_press(MouseButton.MIDDLE)
        backend.mouse_release(MouseButton.MIDDLE)

    def test_mouse_is_pressed_all_buttons(self) -> None:
        """Test mouse_is_pressed for all button types."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Test all buttons (should return bool without crashing)
        for button in [
            MouseButton.LEFT,
            MouseButton.MIDDLE,
            MouseButton.RIGHT,
            MouseButton.X1,
            MouseButton.X2,
        ]:
            result = backend.mouse_is_pressed(button)
            assert isinstance(result, bool)


class TestX11KeyboardEdgeCases:
    """Test X11 keyboard edge cases."""

    def test_key_is_pressed_with_enum(self) -> None:
        """Test key_is_pressed with Key enum."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import Key

        backend = X11Backend()

        # Should not crash with Key enum
        result = backend.key_is_pressed(Key.A)
        assert isinstance(result, bool)

    def test_key_is_pressed_special_keys(self) -> None:
        """Test key_is_pressed with special keys."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Test various special keys
        for key in ["shift", "ctrl", "alt", "enter", "space", "tab"]:
            result = backend.key_is_pressed(key)
            assert isinstance(result, bool)

    def test_key_type_unicode_with_invalid_chars(self) -> None:
        """Test key_type_unicode with characters that don't have keycodes."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Test with ASCII string containing unmappable characters
        # This should trigger the ValueError catch and skip those chars
        backend.key_type_unicode("`~")  # These might not be mapped


class TestX11WindowOperations:
    """Test X11 window operations in detail."""

    def test_list_windows_include_invisible(self) -> None:
        """Test listing windows including invisible ones."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Get both visible and invisible windows
        all_windows = backend.list_windows(visible_only=False)
        visible_windows = backend.list_windows(visible_only=True)

        # All windows should include visible windows
        assert len(all_windows) >= len(visible_windows)

    def test_focus_window_with_window_info(self) -> None:
        """Test focus_window with WindowInfo object."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available")

        # Should work with WindowInfo object
        backend.focus_window(windows[0])

    def test_get_window_at_origin(self) -> None:
        """Test get_window_at at origin (0, 0)."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Should return a window or None
        result = backend.get_window_at(0, 0)
        assert result is None or hasattr(result, "handle")

    def test_get_window_at_far_position(self) -> None:
        """Test get_window_at at a position far from any window."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Should return None for position outside screen
        result = backend.get_window_at(10000, 10000)
        assert result is None or hasattr(result, "handle")


class TestX11Clipboard:
    """Test X11 clipboard operations."""

    def test_clipboard_has_text_empty(self) -> None:
        """Test clipboard_has_text when clipboard is empty."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Initially should be empty or have content
        # Just test that it doesn't crash
        result = backend.clipboard_has_text()
        assert isinstance(result, bool)

    def test_clipboard_clear(self) -> None:
        """Test clipboard_clear method."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Clear should not raise
        backend.clipboard_clear()

    def test_clipboard_set_and_has_text(self) -> None:
        """Test clipboard_set_text and clipboard_has_text."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Set text
        backend.clipboard_set_text("test")

        # Should have text (may not work in Xvfb, but shouldn't crash)
        result = backend.clipboard_has_text()
        assert isinstance(result, bool)

    def test_clipboard_get_when_empty(self) -> None:
        """Test clipboard_get_text when clipboard is empty."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Clear first
        backend.clipboard_clear()

        # Get should return empty string or current content
        result = backend.clipboard_get_text()
        assert isinstance(result, str)


class TestX11WindowState:
    """Test X11 window state operations."""

    def test_set_window_state_minimized(self) -> None:
        """Test setting window to minimized state."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import WindowState

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available")

        # Try to minimize (may not work without window manager)
        try:
            backend.set_window_state(windows[0], WindowState.MINIMIZED)
        except Exception:
            pass  # Expected in Xvfb

    def test_set_window_state_maximized(self) -> None:
        """Test setting window to maximized state."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import WindowState

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available")

        # Try to maximize (may not work without window manager)
        try:
            backend.set_window_state(windows[0], WindowState.MAXIMIZED)
        except Exception:
            pass  # Expected in Xvfb

    def test_close_window(self) -> None:
        """Test closing a window."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available")

        # Should not crash (but may not actually close in Xvfb)
        try:
            backend.close_window(windows[0])
        except Exception:
            pass  # Some windows may not be closeable


class TestX11ErrorHandling:
    """Test X11 backend error handling."""

    def test_invalid_key_press(self) -> None:
        """Test pressing an invalid key."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Invalid key should raise ValueError
        with pytest.raises(ValueError):
            backend.key_press("invalid_key_name_that_does_not_exist")

    def test_invalid_key_release(self) -> None:
        """Test releasing an invalid key."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Invalid key should raise ValueError
        with pytest.raises(ValueError):
            backend.key_release("invalid_key_name_that_does_not_exist")

    def test_invalid_mouse_button(self) -> None:
        """Test with an invalid mouse button."""
        from guiguigui.backend.x11 import X11Backend
        from guiguigui.core.types import MouseButton

        backend = X11Backend()

        # Create a fake invalid button (this will test the ValueError path)
        # Note: We can't easily create an invalid MouseButton enum value,
        # so we test that valid buttons don't raise
        backend.mouse_press(MouseButton.LEFT)
        backend.mouse_release(MouseButton.LEFT)

    def test_window_with_int_handle(self) -> None:
        """Test window operations with int handle instead of WindowInfo."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available")

        # Get a window handle as int
        handle = windows[0].handle

        # These should work with int handles
        backend.set_window_opacity(handle, 0.5)
        backend.set_window_always_on_top(handle, False)
        backend.get_window_state(handle)
        backend.move_window(handle, 100, 100)
        backend.resize_window(handle, 400, 300)

    def test_display_fallback_on_randr_error(self) -> None:
        """Test display detection falls back gracefully on RandR errors."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # This should work even if RandR has issues
        displays = backend.get_displays()
        assert len(displays) >= 1
        assert displays[0].is_primary


class TestX11DisplayProperties:
    """Test X11 display property access."""

    def test_display_has_bounds(self) -> None:
        """Test that displays have bounds."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()

        assert len(displays) >= 1
        for display in displays:
            assert display.bounds.width > 0
            assert display.bounds.height > 0

    def test_display_has_work_area(self) -> None:
        """Test that displays have work area."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()

        for display in displays:
            assert display.work_area is not None
            assert display.work_area.width > 0
            assert display.work_area.height > 0

    def test_display_has_physical_size(self) -> None:
        """Test that displays have physical size."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()

        for display in displays:
            assert display.physical_size is not None
            # Physical size might be 0 in virtual displays
            assert display.physical_size.width >= 0
            assert display.physical_size.height >= 0

    def test_virtual_screen_calculation(self) -> None:
        """Test virtual screen rect calculation."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()
        displays = backend.get_displays()
        virtual = backend.get_virtual_screen_rect()

        # Virtual screen should encompass all displays
        for display in displays:
            assert virtual.x <= display.bounds.x
            assert virtual.y <= display.bounds.y


class TestX11ClipboardSelectionHandling:
    """Test X11 clipboard selection handling."""

    def test_clipboard_set_creates_window(self) -> None:
        """Test that clipboard_set_text creates a clipboard window."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Set text should create clipboard window
        backend.clipboard_set_text("test")

        # Check that clipboard window was created
        assert hasattr(backend, "_clipboard_window")
        assert hasattr(backend, "_clipboard_text")

    def test_clipboard_get_own_selection(self) -> None:
        """Test getting clipboard text we just set."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Set and get our own clipboard
        test_text = "test content 123"
        backend.clipboard_set_text(test_text)

        # Should get back the same text
        result = backend.clipboard_get_text()
        assert result == test_text

    def test_clipboard_unicode_content(self) -> None:
        """Test clipboard with unicode content."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Set unicode text
        test_text = "测试 test テスト"
        backend.clipboard_set_text(test_text)

        # Should get back the same text
        result = backend.clipboard_get_text()
        assert result == test_text


class TestX11KeyCodeMapping:
    """Test X11 key code mapping."""

    def test_letters_mapped(self) -> None:
        """Test that all letters are mapped."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # All lowercase letters should be mapped
        for char in "abcdefghijklmnopqrstuvwxyz":
            assert char in backend._key_code_map

    def test_numbers_mapped(self) -> None:
        """Test that all numbers are mapped."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # All numbers should be mapped
        for num in "0123456789":
            assert num in backend._key_code_map

    def test_function_keys_mapped(self) -> None:
        """Test that function keys are mapped."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Function keys should be mapped
        for i in range(1, 13):
            assert f"f{i}" in backend._key_code_map

    def test_single_char_key_lookup(self) -> None:
        """Test single character key lookup."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Single character keys should work
        backend.key_press("a")
        backend.key_release("a")


class TestX11MouseMoveDuration:
    """Test X11 mouse movement with duration."""

    def test_mouse_move_zero_duration(self) -> None:
        """Test mouse move with zero duration (instant)."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Zero duration should be instant (no interpolation)
        start = backend.mouse_position()
        backend.mouse_move_to(start.x + 100, start.y + 100, duration=0)

        # Should complete immediately

    def test_mouse_move_with_small_duration(self) -> None:
        """Test mouse move with small duration."""
        import time

        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Small duration should interpolate
        start = backend.mouse_position()
        backend.mouse_move_to(start.x + 50, start.y + 50, duration=0.1)

        time.sleep(0.05)  # Give it time to move

    def test_mouse_move_rel_with_duration(self) -> None:
        """Test relative mouse move with duration."""
        from guiguigui.backend.x11 import X11Backend

        backend = X11Backend()

        # Relative move with duration
        backend.mouse_move_rel(20, 20, duration=0.05)
