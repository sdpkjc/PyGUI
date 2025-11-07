from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


@dataclass
class Size:
    width: int
    height: int


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def left(self) -> int:
        return self.x

    @property
    def top(self) -> int:
        return self.y

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(self.x + self.width // 2, self.y + self.height // 2)

    def contains(self, point: Point) -> bool:
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom


class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    X1 = "x1"
    X2 = "x2"


class WindowState(Enum):
    NORMAL = "normal"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"


class Key(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"

    NUM_0 = "0"
    NUM_1 = "1"
    NUM_2 = "2"
    NUM_3 = "3"
    NUM_4 = "4"
    NUM_5 = "5"
    NUM_6 = "6"
    NUM_7 = "7"
    NUM_8 = "8"
    NUM_9 = "9"

    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    F13 = "f13"
    F14 = "f14"
    F15 = "f15"
    F16 = "f16"
    F17 = "f17"
    F18 = "f18"
    F19 = "f19"
    F20 = "f20"

    ENTER = "enter"
    RETURN = "return"
    TAB = "tab"
    SPACE = "space"
    BACKSPACE = "backspace"
    DELETE = "delete"
    ESC = "esc"
    ESCAPE = "escape"

    SHIFT = "shift"
    CTRL = "ctrl"
    CONTROL = "control"
    ALT = "alt"
    OPTION = "option"
    CMD = "cmd"
    COMMAND = "command"
    WIN = "win"
    WINDOWS = "windows"
    SUPER = "super"
    META = "meta"

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    HOME = "home"
    END = "end"
    PAGEUP = "pageup"
    PAGEDOWN = "pagedown"

    CAPSLOCK = "capslock"
    NUMLOCK = "numlock"
    SCROLLLOCK = "scrolllock"


@dataclass
class DisplayInfo:
    id: str
    name: str
    bounds: Rect
    work_area: Rect
    scale: float
    physical_size: Size
    refresh_rate: float
    rotation: int
    is_primary: bool


@dataclass
class WindowInfo:
    handle: Any
    title: str
    class_name: str
    pid: int
    process_name: str
    rect: Rect
    client_rect: Rect
    state: WindowState
    is_visible: bool
    is_active: bool
    is_always_on_top: bool
    opacity: float
    display: DisplayInfo | None = None


@dataclass
class MouseEvent:
    position: Point
    button: MouseButton | None
    pressed: bool
    timestamp: float


@dataclass
class KeyboardEvent:
    key: Key | str
    pressed: bool
    modifiers: set[Key]
    timestamp: float
