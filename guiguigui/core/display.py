from __future__ import annotations

from ..backend import get_backend
from .types import DisplayInfo, Point, Rect


class Display:
    def __init__(self):
        self._backend = get_backend()

    def all(self) -> list[DisplayInfo]:
        return self._backend.get_displays()

    # Alias for consistency with other modules
    def list(self) -> list[DisplayInfo]:
        """Alias for all()"""
        return self.all()

    def primary(self) -> DisplayInfo:
        return self._backend.get_primary_display()

    def count(self) -> int:
        return len(self.all())

    def at_point(self, x: int, y: int) -> DisplayInfo | None:
        point = Point(x, y)
        for display in self.all():
            if display.bounds.contains(point):
                return display
        return None

    # Alias for shorter API
    def at(self, x: int, y: int) -> DisplayInfo | None:
        """Alias for at_point()"""
        return self.at_point(x, y)

    def virtual_rect(self) -> Rect:
        return self._backend.get_virtual_screen_rect()

    # Alias for consistency
    def virtual_screen_rect(self) -> Rect:
        """Alias for virtual_rect()"""
        return self.virtual_rect()

    def to_physical(self, point: Point, display: DisplayInfo | None = None) -> Point:
        if display is None:
            display = self.at_point(point.x, point.y)
            if display is None:
                display = self.primary()

        rel_x = point.x - display.bounds.x
        rel_y = point.y - display.bounds.y

        phys_x = int(rel_x * display.scale)
        phys_y = int(rel_y * display.scale)

        return Point(display.bounds.x + phys_x, display.bounds.y + phys_y)

    def from_physical(self, point: Point, display: DisplayInfo | None = None) -> Point:
        if display is None:
            for d in self.all():
                phys_bounds = Rect(
                    d.bounds.x,
                    d.bounds.y,
                    int(d.bounds.width * d.scale),
                    int(d.bounds.height * d.scale),
                )
                if phys_bounds.contains(point):
                    display = d
                    break
            if display is None:
                display = self.primary()

        rel_x = point.x - display.bounds.x
        rel_y = point.y - display.bounds.y

        log_x = int(rel_x / display.scale)
        log_y = int(rel_y / display.scale)

        return Point(display.bounds.x + log_x, display.bounds.y + log_y)


display = Display()
