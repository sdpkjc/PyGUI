from __future__ import annotations

import sys

import pytest

from guiguigui import clipboard


@pytest.mark.integration
@pytest.mark.skipif(sys.platform.startswith("linux"), reason="X11 clipboard not yet implemented")
class TestClipboardOperations:
    def test_set_and_get_text(self) -> None:
        original = clipboard.get()

        test_text = "Test clipboard content"
        clipboard.set(test_text)
        assert clipboard.get() == test_text

        clipboard.set(original)

    def test_set_and_get_unicode(self) -> None:
        original = clipboard.get()

        test_text = "Unicode text: 你好世界 🌍 こんにちは"
        clipboard.set(test_text)
        assert clipboard.get() == test_text

        clipboard.set(original)

    def test_clear_clipboard(self) -> None:
        original = clipboard.get()

        clipboard.set("Some content")
        assert clipboard.has_text()

        clipboard.clear()
        assert not clipboard.has_text()
        assert clipboard.get() == ""

        clipboard.set(original)

    def test_has_text(self) -> None:
        original = clipboard.get()

        clipboard.set("Content")
        assert clipboard.has_text()

        clipboard.clear()
        assert not clipboard.has_text()

        clipboard.set(original)

    def test_empty_string(self) -> None:
        original = clipboard.get()

        clipboard.set("")
        assert clipboard.get() == ""
        assert not clipboard.has_text()

        clipboard.set(original)

    def test_multiline_text(self) -> None:
        original = clipboard.get()

        test_text = "Line 1\nLine 2\nLine 3"
        clipboard.set(test_text)
        assert clipboard.get() == test_text

        clipboard.set(original)

    def test_special_characters(self) -> None:
        original = clipboard.get()

        test_text = "Special: \t\n\r!@#$%^&*()_+-=[]{}|;:',.<>?/"
        clipboard.set(test_text)
        assert clipboard.get() == test_text

        clipboard.set(original)
