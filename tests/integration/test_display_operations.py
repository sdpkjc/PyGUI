from __future__ import annotations

import pytest

from guiguigui import display
from guiguigui.core.types import DisplayInfo, Rect


@pytest.mark.integration
class TestDisplayOperations:
    def test_list_displays(self) -> None:
        displays = display.list()
        assert isinstance(displays, list)
        assert len(displays) >= 1
        assert all(isinstance(d, DisplayInfo) for d in displays)

    def test_primary_display(self) -> None:
        primary = display.primary()
        assert isinstance(primary, DisplayInfo)
        assert primary.is_primary
        assert primary.bounds.width > 0
        assert primary.bounds.height > 0

    def test_display_count(self) -> None:
        count = display.count()
        assert isinstance(count, int)
        assert count >= 1

    def test_virtual_screen_rect(self) -> None:
        virtual = display.virtual_screen_rect()
        assert isinstance(virtual, Rect)
        assert virtual.width > 0
        assert virtual.height > 0

    def test_display_properties(self) -> None:
        displays = display.list()
        for disp in displays:
            assert isinstance(disp.id, str)
            assert len(disp.id) > 0
            assert isinstance(disp.name, str)
            assert disp.bounds.width > 0
            assert disp.bounds.height > 0
            assert disp.scale > 0
            assert disp.physical_size.width > 0
            assert disp.physical_size.height > 0
            assert disp.refresh_rate > 0
            assert disp.rotation in [0, 90, 180, 270]

    def test_display_work_area(self) -> None:
        primary = display.primary()
        assert primary.work_area.width > 0
        assert primary.work_area.height > 0
        assert primary.work_area.width <= primary.bounds.width
        assert primary.work_area.height <= primary.bounds.height

    def test_get_display_at_primary(self) -> None:
        primary = display.primary()
        center = primary.bounds.center
        disp_at_center = display.at(center.x, center.y)
        assert disp_at_center is not None
        assert disp_at_center.id == primary.id

    def test_virtual_screen_covers_all_displays(self) -> None:
        displays = display.list()
        virtual = display.virtual_screen_rect()

        for disp in displays:
            assert virtual.left <= disp.bounds.left
            assert virtual.top <= disp.bounds.top
            assert virtual.right >= disp.bounds.right
            assert virtual.bottom >= disp.bounds.bottom
