from __future__ import annotations

from pygui.core.clipboard import Clipboard
from tests.conftest import MockBackend


class TestClipboard:
    def test_get_text(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        mock_backend._clipboard_text = "Hello, World!"
        assert clipboard.get() == "Hello, World!"

    def test_set_text(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        clipboard.set("Test text")
        assert mock_backend._clipboard_text == "Test text"

    def test_clear(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        mock_backend._clipboard_text = "Some text"
        clipboard.clear()
        assert mock_backend._clipboard_text == ""

    def test_has_text_true(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        mock_backend._clipboard_text = "Content"
        assert clipboard.has_text()

    def test_has_text_false(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        mock_backend._clipboard_text = ""
        assert not clipboard.has_text()

    def test_set_and_get_unicode(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        text = "你好世界 🌍"
        clipboard.set(text)
        assert clipboard.get() == text

    def test_empty_clipboard(self, mock_backend: MockBackend) -> None:
        clipboard = Clipboard()
        assert clipboard.get() == ""
        assert not clipboard.has_text()
