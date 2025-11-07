from __future__ import annotations

from pygui.core.display import Display
from pygui.core.types import Rect
from tests.conftest import MockBackend


class TestDisplay:
    def test_list_all_displays(self, mock_backend: MockBackend) -> None:
        display = Display()
        displays = display.list()
        assert len(displays) == 2
        assert displays[0].id == "display0"
        assert displays[1].id == "display1"

    def test_primary_display(self, mock_backend: MockBackend) -> None:
        display = Display()
        primary = display.primary()
        assert primary.is_primary
        assert primary.id == "display0"
        assert primary.bounds == Rect(0, 0, 1920, 1080)

    def test_get_display_at(self, mock_backend: MockBackend) -> None:
        display = Display()
        disp = display.at(100, 100)
        assert disp is not None
        assert disp.id == "display0"

    def test_get_display_at_second_monitor(self, mock_backend: MockBackend) -> None:
        display = Display()
        disp = display.at(2000, 100)
        assert disp is not None
        assert disp.id == "display1"

    def test_get_display_at_outside_bounds(self, mock_backend: MockBackend) -> None:
        display = Display()
        disp = display.at(10000, 10000)
        assert disp is None

    def test_virtual_screen_rect(self, mock_backend: MockBackend) -> None:
        display = Display()
        virtual = display.virtual_screen_rect()
        assert virtual == Rect(0, 0, 3840, 1080)

    def test_display_count(self, mock_backend: MockBackend) -> None:
        display = Display()
        assert display.count() == 2

    def test_display_properties(self, mock_backend: MockBackend) -> None:
        display = Display()
        primary = display.primary()
        assert primary.name == "Main Display"
        assert primary.scale == 1.0
        assert primary.physical_size.width == 1920
        assert primary.physical_size.height == 1080
        assert primary.refresh_rate == 60.0
        assert primary.rotation == 0
        assert primary.work_area.height == 1040

    def test_secondary_display_properties(self, mock_backend: MockBackend) -> None:
        display = Display()
        displays = display.list()
        secondary = displays[1]
        assert not secondary.is_primary
        assert secondary.scale == 2.0
        assert secondary.bounds == Rect(1920, 0, 1920, 1080)
