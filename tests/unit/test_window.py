from __future__ import annotations

from guiguigui.core.types import Rect, WindowInfo, WindowState
from guiguigui.core.window import Window
from tests.conftest import MockBackend


class TestWindow:
    def setup_method(self) -> None:
        pass

    def test_list_all_windows(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Window 1",
            class_name="Class1",
            pid=100,
            process_name="app1",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        win2 = WindowInfo(
            handle=2,
            title="Window 2",
            class_name="Class2",
            pid=200,
            process_name="app2",
            rect=Rect(100, 100, 600, 400),
            client_rect=Rect(100, 100, 600, 400),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1, win2]

        windows = window.list()
        assert len(windows) == 2
        assert windows[0].title == "Window 1"
        assert windows[1].title == "Window 2"

    def test_list_visible_only(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Visible",
            class_name="Class1",
            pid=100,
            process_name="app1",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        win2 = WindowInfo(
            handle=2,
            title="Hidden",
            class_name="Class2",
            pid=200,
            process_name="app2",
            rect=Rect(100, 100, 600, 400),
            client_rect=Rect(100, 100, 600, 400),
            state=WindowState.NORMAL,
            is_visible=False,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1, win2]

        visible_windows = window.list(visible_only=True)
        assert len(visible_windows) == 1
        assert visible_windows[0].title == "Visible"

        all_windows = window.list(visible_only=False)
        assert len(all_windows) == 2

    def test_find_by_title(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Test Application",
            class_name="Class1",
            pid=100,
            process_name="app1",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1]

        found = window.find(title="Test Application")
        assert found is not None
        assert found.title == "Test Application"

    def test_find_by_title_regex(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="My Application v1.0",
            class_name="Class1",
            pid=100,
            process_name="app1",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1]

        found = window.find(title="Application.*", regex=True)
        assert found is not None
        assert "Application" in found.title

    def test_find_by_class_name(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Window",
            class_name="TestClass",
            pid=100,
            process_name="app1",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1]

        found = window.find(class_name="TestClass")
        assert found is not None
        assert found.class_name == "TestClass"

    def test_find_by_process(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Window",
            class_name="Class",
            pid=100,
            process_name="my_app",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1]

        found = window.find(process_name="my_app")
        assert found is not None
        assert found.process_name == "my_app"

    def test_find_not_found(self, mock_backend: MockBackend) -> None:
        window = Window()
        mock_backend._windows = []

        found = window.find(title="NonExistent")
        assert found is None

    def test_active_window(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Active",
            class_name="Class",
            pid=100,
            process_name="app",
            rect=Rect(0, 0, 800, 600),
            client_rect=Rect(0, 0, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=True,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._active_window = win1

        active = window.active()
        assert active is not None
        assert active.title == "Active"

    def test_window_at_position(self, mock_backend: MockBackend) -> None:
        window = Window()
        win1 = WindowInfo(
            handle=1,
            title="Window",
            class_name="Class",
            pid=100,
            process_name="app",
            rect=Rect(100, 100, 800, 600),
            client_rect=Rect(100, 100, 800, 600),
            state=WindowState.NORMAL,
            is_visible=True,
            is_active=False,
            is_always_on_top=False,
            opacity=1.0,
        )
        mock_backend._windows = [win1]

        found = window.at(200, 200)
        assert found is not None
        assert found.title == "Window"

    def test_focus_window(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.focus(sample_window)
        assert mock_backend._active_window == sample_window

    def test_move_window(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.move(sample_window, 200, 300)
        assert sample_window.rect.x == 200
        assert sample_window.rect.y == 300

    def test_resize_window(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.resize(sample_window, 1024, 768)
        assert sample_window.rect.width == 1024
        assert sample_window.rect.height == 768

    def test_set_state(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.set_state(sample_window, WindowState.MAXIMIZED)
        assert sample_window.state == WindowState.MAXIMIZED

    def test_get_state(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]
        sample_window.state = WindowState.MINIMIZED

        state = window.get_state(sample_window)
        assert state == WindowState.MINIMIZED

    def test_close_window(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.close(sample_window)
        assert len(mock_backend._windows) == 0

    def test_set_opacity(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.set_opacity(sample_window, 0.5)
        assert sample_window.opacity == 0.5

    def test_set_always_on_top(self, mock_backend: MockBackend, sample_window: WindowInfo) -> None:
        window = Window()
        mock_backend._windows = [sample_window]

        window.set_always_on_top(sample_window, True)
        assert sample_window.is_always_on_top
