from .core.clipboard import clipboard
from .core.display import display
from .core.events import events
from .core.keyboard import keyboard
from .core.macro import Macro, macro
from .core.mouse import mouse
from .core.types import DisplayInfo, Key, MouseButton, Point, Rect, Size, WindowInfo, WindowState
from .core.window import window

__version__ = "0.1.0"

__all__ = [
    "mouse",
    "keyboard",
    "display",
    "window",
    "clipboard",
    "events",
    "Macro",
    "macro",
    "Point",
    "Size",
    "Rect",
    "MouseButton",
    "WindowState",
    "Key",
    "DisplayInfo",
    "WindowInfo",
]
