"""Unit tests for macOS backend implementation.

These tests verify the macOS-specific backend logic and methods.
"""

from __future__ import annotations

import sys

import pytest

# Only run these tests on macOS
pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="macOS only tests")


class TestMacOSBackendImport:
    """Test macOS backend can be imported and instantiated."""

    def test_import_macos_backend(self) -> None:
        """Test that macOS backend can be imported."""
        from guiguigui.backend.macos import MacOSBackend

        assert MacOSBackend is not None

    def test_create_macos_backend(self) -> None:
        """Test that macOS backend can be instantiated."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        assert backend is not None

    def test_backend_has_required_methods(self) -> None:
        """Test that backend implements all required abstract methods."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

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


class TestMacOSKeyMapping:
    """Test key code mapping for macOS."""

    def test_key_mapping_exists(self) -> None:
        """Test that key mapping dictionary exists."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        # Check that _key_code_map is defined
        assert hasattr(backend, "_key_code_map")
        assert isinstance(backend._key_code_map, dict)

    def test_common_keys_mapped(self) -> None:
        """Test that common keys have mappings."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Test some common keys exist in mapping
        common_keys = [
            "a",
            "return",
            "space",
            "shift",
            "command",
            "escape",
            "delete",
        ]

        for key in common_keys:
            assert key in backend._key_code_map, f"Key {key} should be in key code map"


class TestMacOSMouseButton:
    """Test mouse button operations for macOS."""

    def test_mouse_button_press_release(self) -> None:
        """Test mouse button press and release operations."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # These should not raise exceptions
        # Just test that the methods work
        backend.mouse_press(MouseButton.LEFT)
        backend.mouse_release(MouseButton.LEFT)

    def test_mouse_is_pressed_returns_bool(self) -> None:
        """Test that mouse_is_pressed returns a boolean."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import MouseButton

        backend = MacOSBackend()

        # Should return a boolean for all button types
        result_left = backend.mouse_is_pressed(MouseButton.LEFT)
        result_right = backend.mouse_is_pressed(MouseButton.RIGHT)
        result_middle = backend.mouse_is_pressed(MouseButton.MIDDLE)

        assert isinstance(result_left, bool)
        assert isinstance(result_right, bool)
        assert isinstance(result_middle, bool)


class TestMacOSPermissions:
    """Test permission checking on macOS."""

    def test_check_permissions_returns_dict(self) -> None:
        """Test that check_permissions returns a dictionary."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        try:
            perms = backend.check_permissions()

            assert isinstance(perms, dict)
            assert "accessibility" in perms
            assert "screen_recording" in perms
            assert isinstance(perms["accessibility"], bool)
            assert isinstance(perms["screen_recording"], bool)
        except AttributeError:
            # AXIsProcessTrusted might not be available in some environments
            pytest.skip("Permission check API not available")


class TestMacOSKeyboard:
    """Test keyboard operations for macOS."""

    def test_key_is_pressed_returns_bool(self) -> None:
        """Test that key_is_pressed returns a boolean."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import Key

        backend = MacOSBackend()

        # Should return a boolean for various key types
        result_shift = backend.key_is_pressed(Key.SHIFT)
        result_a = backend.key_is_pressed("a")
        result_space = backend.key_is_pressed(Key.SPACE)

        assert isinstance(result_shift, bool)
        assert isinstance(result_a, bool)
        assert isinstance(result_space, bool)


class TestMacOSKeyboardLayout:
    """Test keyboard layout detection."""

    def test_get_keyboard_layout_returns_string(self) -> None:
        """Test that get_keyboard_layout returns a string."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        layout = backend.get_keyboard_layout()

        assert isinstance(layout, str)
        assert len(layout) > 0

    def test_keyboard_layout_format(self) -> None:
        """Test that keyboard layout has expected format."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        layout = backend.get_keyboard_layout()

        # Should be something like "com.apple.keylayout.US"
        assert "." in layout or layout != ""


class TestMacOSDisplay:
    """Test display-related methods."""

    def test_get_displays_returns_list(self) -> None:
        """Test that get_displays returns a list."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        displays = backend.get_displays()

        assert isinstance(displays, list)
        assert len(displays) > 0

    def test_display_info_structure(self) -> None:
        """Test that DisplayInfo has correct structure."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
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
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        primary = backend.get_primary_display()

        assert primary is not None
        assert primary.is_primary is True

    def test_virtual_screen_rect(self) -> None:
        """Test virtual screen rect calculation."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        rect = backend.get_virtual_screen_rect()

        assert rect.width > 0
        assert rect.height > 0


class TestMacOSClipboard:
    """Test clipboard operations."""

    def test_clipboard_set_and_get(self) -> None:
        """Test setting and getting clipboard text."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Save original
        original = backend.clipboard_get_text()

        # Test set and get
        test_text = "GuiGuiGui Test"
        backend.clipboard_set_text(test_text)
        result = backend.clipboard_get_text()

        assert result == test_text

        # Restore original
        backend.clipboard_set_text(original)

    def test_clipboard_has_text(self) -> None:
        """Test checking if clipboard has text."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        backend.clipboard_set_text("test")
        assert backend.clipboard_has_text() is True

        backend.clipboard_clear()
        # After clear, might still have text or not depending on system
        # Just check it returns a boolean
        assert isinstance(backend.clipboard_has_text(), bool)

    def test_clipboard_clear(self) -> None:
        """Test clearing clipboard."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        backend.clipboard_set_text("test")
        backend.clipboard_clear()

        # Clear should work without error
        assert True


class TestMacOSWindow:
    """Test window-related methods."""

    def test_list_windows_returns_list(self) -> None:
        """Test that list_windows returns a list."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        windows = backend.list_windows()

        assert isinstance(windows, list)

    def test_get_active_window(self) -> None:
        """Test getting active window."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        active = backend.get_active_window()

        # Might be None if no windows, but should not raise
        if active:
            assert hasattr(active, "title")
            assert hasattr(active, "handle")

    def test_window_manipulation_raises_capability_error(self) -> None:
        """Test that window manipulation methods raise BackendCapabilityError on macOS."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.errors import BackendCapabilityError
        from guiguigui.core.types import WindowState

        backend = MacOSBackend()

        # Get a window handle (or use a dummy value if no windows)
        windows = backend.list_windows()
        if not windows:
            pytest.skip("No windows available for testing")

        handle = windows[0].handle

        # These methods should raise BackendCapabilityError on macOS
        with pytest.raises(BackendCapabilityError):
            backend.move_window(handle, 100, 100)

        with pytest.raises(BackendCapabilityError):
            backend.resize_window(handle, 800, 600)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_state(handle, WindowState.MAXIMIZED)

        with pytest.raises(BackendCapabilityError):
            backend.close_window(handle)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_opacity(handle, 0.8)

        with pytest.raises(BackendCapabilityError):
            backend.set_window_always_on_top(handle, True)

    def test_window_get_state(self) -> None:
        """Test that get_window_state returns a WindowState."""
        from guiguigui.backend.macos import MacOSBackend
        from guiguigui.core.types import WindowState

        backend = MacOSBackend()
        windows = backend.list_windows()

        if not windows:
            pytest.skip("No windows available for testing")

        handle = windows[0].handle

        # get_window_state should not raise, but always returns NORMAL on macOS
        state = backend.get_window_state(handle)
        assert isinstance(state, WindowState)
        assert state == WindowState.NORMAL


class TestMacOSEventHooks:
    """Test event hook methods."""

    def test_hook_methods_raise_not_implemented(self) -> None:
        """Test that hook methods raise NotImplementedError."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()

        # Hook methods should raise NotImplementedError
        with pytest.raises(NotImplementedError):
            backend.hook_mouse(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.hook_keyboard(lambda event: True)

        with pytest.raises(NotImplementedError):
            backend.unhook(None)


class TestMacOSCoordinateSystem:
    """Test coordinate system handling."""

    def test_mouse_position_in_bounds(self) -> None:
        """Test that mouse position is within screen bounds."""
        from guiguigui.backend.macos import MacOSBackend

        backend = MacOSBackend()
        pos = backend.mouse_position()
        rect = backend.get_virtual_screen_rect()

        # Position should be within virtual screen
        assert pos.x >= rect.x
        assert pos.y >= rect.y
        # Allow some margin for multi-monitor setups
        assert pos.x <= rect.x + rect.width + 1000
        assert pos.y <= rect.y + rect.height + 1000
