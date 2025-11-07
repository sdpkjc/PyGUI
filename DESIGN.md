# GuiGuiGui 技术设计文档

## 0. 项目定位与目标

**GuiGuiGui** 是一个极简的跨平台 GUI 自动化控制库，专注于提供完备的底层 GUI 操作接口。

### 核心原则

> **只做输入控制、窗口管理、显示器管理、剪贴板和事件钩子**
> **不做图像匹配、OCR、UI元素识别等高层功能**

### 设计目标

1. **跨平台支持**：macOS / Linux (X11 + Wayland) / Windows
2. **完备的 GUI 操作**（在权限允许范围内）
3. **多显示器和高 DPI 支持**
4. **强大的窗口管理能力**
5. **优雅的宏操作抽象**
6. **极简主义设计**

---

## 1. 架构设计

### 1.1 目录结构

```
guiguigui/
├── guiguigui/
│   ├── __init__.py              # 统一API入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── types.py             # 数据类型定义
│   │   ├── mouse.py             # 鼠标操作抽象层
│   │   ├── keyboard.py          # 键盘操作抽象层
│   │   ├── window.py            # 窗口管理抽象层
│   │   ├── display.py           # 显示器管理抽象层
│   │   ├── clipboard.py         # 剪贴板抽象层
│   │   ├── events.py            # 事件监听/钩子
│   │   ├── macro.py             # 宏系统
│   │   └── errors.py            # 异常定义
│   ├── backend/
│   │   ├── __init__.py          # 后端加载器
│   │   ├── base.py              # 抽象基类
│   │   ├── win32.py             # Windows 实现
│   │   ├── macos.py             # macOS 实现
│   │   ├── x11.py               # Linux X11 实现
│   │   └── wayland.py           # Linux Wayland 实现
│   └── util/
│       ├── __init__.py
│       ├── platform.py          # 平台检测
│       ├── dpi.py               # DPI 转换工具
│       ├── timing.py            # 延迟/重试工具
│       └── logger.py            # 日志
├── tests/
│   ├── unit/                    # 单元测试
│   ├── integration/             # 集成测试
│   └── platform/                # 平台特定测试
├── examples/
│   ├── basic_operations.py
│   ├── multi_monitor.py
│   ├── window_management.py
│   └── macro_examples.py
├── docs/
│   ├── api.md
│   ├── platform_notes.md
│   └── migration.md
├── pyproject.toml
├── README.md
└── DESIGN.md
```

### 1.2 API 入口设计

```python
# guiguigui/__init__.py
from .core.mouse import mouse
from .core.keyboard import keyboard
from .core.window import window
from .core.display import display
from .core.clipboard import clipboard
from .core.macro import Macro, macro
from .core.events import events

__all__ = [
    "mouse",
    "keyboard",
    "window",
    "display",
    "clipboard",
    "Macro",
    "macro",
    "events",
]
```

---

## 2. 核心类型定义

### 2.1 基础类型（core/types.py）

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any

@dataclass
class Point:
    """坐标点（逻辑坐标）"""
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

@dataclass
class Size:
    """尺寸"""
    width: int
    height: int

@dataclass
class Rect:
    """矩形区域"""
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
        """判断点是否在矩形内"""
        return (self.left <= point.x <= self.right and
                self.top <= point.y <= self.bottom)

class MouseButton(Enum):
    """鼠标按键"""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    X1 = "x1"  # 侧键1
    X2 = "x2"  # 侧键2

class WindowState(Enum):
    """窗口状态"""
    NORMAL = "normal"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"

class Key(Enum):
    """键盘按键统一枚举"""
    # 字母
    A = "a"
    B = "b"
    C = "c"
    # ... 其他字母

    # 数字
    NUM_0 = "0"
    NUM_1 = "1"
    # ... 其他数字

    # 功能键
    F1 = "f1"
    F2 = "f2"
    # ... F1-F24

    # 控制键
    ENTER = "enter"
    RETURN = "return"
    TAB = "tab"
    SPACE = "space"
    BACKSPACE = "backspace"
    DELETE = "delete"
    ESC = "esc"
    ESCAPE = "escape"

    # 修饰键
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

    # 方向键
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    # 导航键
    HOME = "home"
    END = "end"
    PAGEUP = "pageup"
    PAGEDOWN = "pagedown"

    # 锁定键
    CAPSLOCK = "capslock"
    NUMLOCK = "numlock"
    SCROLLLOCK = "scrolllock"

@dataclass
class DisplayInfo:
    """显示器信息"""
    id: str
    name: str
    bounds: Rect              # 在虚拟桌面中的位置
    work_area: Rect           # 可用区域（排除任务栏等）
    scale: float              # DPI 缩放比例（1.0 = 100%, 2.0 = 200%）
    physical_size: Size       # 物理分辨率
    refresh_rate: float       # 刷新率 (Hz)
    rotation: int             # 旋转角度 (0, 90, 180, 270)
    is_primary: bool          # 是否主显示器

@dataclass
class WindowInfo:
    """窗口信息"""
    handle: Any               # 平台相关的窗口句柄
    title: str                # 窗口标题
    class_name: str           # 窗口类名（Windows）/ 应用名（其他平台）
    pid: int                  # 进程ID
    process_name: str         # 进程名
    rect: Rect                # 窗口矩形
    client_rect: Rect         # 客户区矩形
    state: WindowState        # 窗口状态
    is_visible: bool          # 是否可见
    is_active: bool           # 是否激活
    is_always_on_top: bool    # 是否置顶
    opacity: float            # 不透明度 (0.0-1.0)
    display: DisplayInfo      # 所在显示器

@dataclass
class MouseEvent:
    """鼠标事件"""
    position: Point
    button: MouseButton | None
    pressed: bool
    timestamp: float

@dataclass
class KeyboardEvent:
    """键盘事件"""
    key: Key | str
    pressed: bool
    modifiers: set[Key]       # 修饰键状态
    timestamp: float
```

---

## 3. 后端抽象层

### 3.1 后端基类（backend/base.py）

```python
from abc import ABC, abstractmethod
from typing import Callable
from ..core.types import *

class Backend(ABC):
    """所有平台后端必须实现的接口"""

    # ============ 鼠标操作 ============

    @abstractmethod
    def mouse_position(self) -> Point:
        """获取鼠标当前位置（逻辑坐标）"""
        pass

    @abstractmethod
    def mouse_move_to(self, x: int, y: int) -> None:
        """移动鼠标到绝对坐标"""
        pass

    @abstractmethod
    def mouse_move_rel(self, dx: int, dy: int) -> None:
        """相对移动鼠标"""
        pass

    @abstractmethod
    def mouse_press(self, button: MouseButton) -> None:
        """按下鼠标按键"""
        pass

    @abstractmethod
    def mouse_release(self, button: MouseButton) -> None:
        """释放鼠标按键"""
        pass

    @abstractmethod
    def mouse_scroll(self, dx: int, dy: int) -> None:
        """滚动鼠标滚轮（dx: 横向, dy: 纵向）"""
        pass

    @abstractmethod
    def mouse_is_pressed(self, button: MouseButton) -> bool:
        """检查按键是否按下"""
        pass

    # ============ 键盘操作 ============

    @abstractmethod
    def key_press(self, key: Key | str) -> None:
        """按下按键"""
        pass

    @abstractmethod
    def key_release(self, key: Key | str) -> None:
        """释放按键"""
        pass

    @abstractmethod
    def key_is_pressed(self, key: Key | str) -> bool:
        """检查按键是否按下"""
        pass

    @abstractmethod
    def key_type_unicode(self, text: str) -> None:
        """输入Unicode文本（优先使用）"""
        pass

    @abstractmethod
    def get_keyboard_layout(self) -> str:
        """获取当前键盘布局"""
        pass

    # ============ 显示器管理 ============

    @abstractmethod
    def get_displays(self) -> list[DisplayInfo]:
        """获取所有显示器信息"""
        pass

    @abstractmethod
    def get_primary_display(self) -> DisplayInfo:
        """获取主显示器"""
        pass

    @abstractmethod
    def get_virtual_screen_rect(self) -> Rect:
        """获取虚拟屏幕矩形（所有显示器组成的总区域）"""
        pass

    # ============ 窗口管理 ============

    @abstractmethod
    def list_windows(self, visible_only: bool = True) -> list[WindowInfo]:
        """列出所有窗口"""
        pass

    @abstractmethod
    def get_active_window(self) -> WindowInfo | None:
        """获取当前激活的窗口"""
        pass

    @abstractmethod
    def get_window_at(self, x: int, y: int) -> WindowInfo | None:
        """获取指定坐标处的窗口"""
        pass

    @abstractmethod
    def focus_window(self, handle: Any) -> None:
        """激活/聚焦窗口"""
        pass

    @abstractmethod
    def move_window(self, handle: Any, x: int, y: int) -> None:
        """移动窗口"""
        pass

    @abstractmethod
    def resize_window(self, handle: Any, width: int, height: int) -> None:
        """调整窗口大小"""
        pass

    @abstractmethod
    def set_window_state(self, handle: Any, state: WindowState) -> None:
        """设置窗口状态"""
        pass

    @abstractmethod
    def get_window_state(self, handle: Any) -> WindowState:
        """获取窗口状态"""
        pass

    @abstractmethod
    def close_window(self, handle: Any) -> None:
        """关闭窗口"""
        pass

    @abstractmethod
    def set_window_opacity(self, handle: Any, opacity: float) -> None:
        """设置窗口不透明度 (0.0-1.0)"""
        pass

    @abstractmethod
    def set_window_always_on_top(self, handle: Any, enabled: bool) -> None:
        """设置窗口置顶"""
        pass

    # ============ 剪贴板 ============

    @abstractmethod
    def clipboard_get_text(self) -> str:
        """获取剪贴板文本"""
        pass

    @abstractmethod
    def clipboard_set_text(self, text: str) -> None:
        """设置剪贴板文本"""
        pass

    @abstractmethod
    def clipboard_clear(self) -> None:
        """清空剪贴板"""
        pass

    @abstractmethod
    def clipboard_has_text(self) -> bool:
        """检查剪贴板是否有文本"""
        pass

    # ============ 事件监听（可选实现） ============

    def hook_mouse(self, callback: Callable[[MouseEvent], bool]) -> Any:
        """注册全局鼠标钩子，返回hook句柄
        callback返回False时阻止事件传递
        """
        raise NotImplementedError("Mouse hook not supported on this platform")

    def hook_keyboard(self, callback: Callable[[KeyboardEvent], bool]) -> Any:
        """注册全局键盘钩子，返回hook句柄
        callback返回False时阻止事件传递
        """
        raise NotImplementedError("Keyboard hook not supported on this platform")

    def unhook(self, hook_handle: Any) -> None:
        """取消钩子"""
        raise NotImplementedError("Hook not supported on this platform")

    # ============ 权限检查 ============

    @abstractmethod
    def check_permissions(self) -> dict[str, bool]:
        """检查各项功能权限
        返回: {
            "mouse": True/False,
            "keyboard": True/False,
            "window": True/False,
            "accessibility": True/False,
        }
        """
        pass
```

### 3.2 后端加载器（backend/__init__.py）

```python
import sys
from .base import Backend

_backend: Backend | None = None

def get_backend() -> Backend:
    """获取当前平台的后端实例（单例）"""
    global _backend
    if _backend is None:
        _backend = _load_backend()
    return _backend

def _load_backend() -> Backend:
    """根据平台加载对应后端"""
    platform = sys.platform

    if platform == "darwin":
        from .macos import MacOSBackend
        return MacOSBackend()

    elif platform == "win32":
        from .win32 import Win32Backend
        return Win32Backend()

    elif platform.startswith("linux"):
        # 检测显示服务器类型
        import os
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        xdg_session_type = os.environ.get("XDG_SESSION_TYPE")

        if wayland_display or xdg_session_type == "wayland":
            try:
                from .wayland import WaylandBackend
                return WaylandBackend()
            except ImportError:
                # 降级到 X11
                pass

        from .x11 import X11Backend
        return X11Backend()

    else:
        raise NotImplementedError(f"Platform {platform} is not supported")
```

---

## 4. 核心模块设计

### 4.1 鼠标模块（core/mouse.py）

```python
import time
import math
from typing import Callable
from ..backend import get_backend
from .types import Point, MouseButton

class Mouse:
    """鼠标操作统一接口"""

    def __init__(self):
        self._backend = get_backend()

    # ============ 基础操作 ============

    def position(self) -> Point:
        """获取鼠标位置"""
        return self._backend.mouse_position()

    def move(self, x: int, y: int, duration: float = 0.0,
             easing: Callable[[float], float] | None = None) -> None:
        """移动鼠标到指定位置

        Args:
            x, y: 目标坐标
            duration: 移动时间（秒），0表示瞬移
            easing: 缓动函数，接受0-1返回0-1
        """
        if duration <= 0:
            self._backend.mouse_move_to(x, y)
            return

        start = self.position()
        steps = max(int(duration * 60), 2)  # 假设60fps

        for i in range(steps + 1):
            t = i / steps
            if easing:
                t = easing(t)

            current_x = int(start.x + (x - start.x) * t)
            current_y = int(start.y + (y - start.y) * t)
            self._backend.mouse_move_to(current_x, current_y)
            time.sleep(duration / steps)

    def move_rel(self, dx: int, dy: int, duration: float = 0.0) -> None:
        """相对移动"""
        if duration <= 0:
            self._backend.mouse_move_rel(dx, dy)
        else:
            current = self.position()
            self.move(current.x + dx, current.y + dy, duration)

    # ============ 点击操作 ============

    def click(self, button: MouseButton | str = MouseButton.LEFT,
              clicks: int = 1, interval: float = 0.1) -> None:
        """点击鼠标

        Args:
            button: 鼠标按键
            clicks: 点击次数
            interval: 多次点击的间隔时间
        """
        if isinstance(button, str):
            button = MouseButton(button)

        for i in range(clicks):
            self._backend.mouse_press(button)
            time.sleep(0.02)  # 短暂延迟确保注册
            self._backend.mouse_release(button)
            if i < clicks - 1:
                time.sleep(interval)

    def double_click(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        """双击"""
        self.click(button, clicks=2, interval=0.1)

    def triple_click(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        """三击"""
        self.click(button, clicks=3, interval=0.1)

    def right_click(self) -> None:
        """右键点击"""
        self.click(MouseButton.RIGHT)

    def middle_click(self) -> None:
        """中键点击"""
        self.click(MouseButton.MIDDLE)

    # ============ 按下/释放 ============

    def press(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        """按下鼠标按键"""
        if isinstance(button, str):
            button = MouseButton(button)
        self._backend.mouse_press(button)

    def release(self, button: MouseButton | str = MouseButton.LEFT) -> None:
        """释放鼠标按键"""
        if isinstance(button, str):
            button = MouseButton(button)
        self._backend.mouse_release(button)

    def is_pressed(self, button: MouseButton | str = MouseButton.LEFT) -> bool:
        """检查按键是否按下"""
        if isinstance(button, str):
            button = MouseButton(button)
        return self._backend.mouse_is_pressed(button)

    # ============ 拖拽 ============

    def drag(self, x: int, y: int, button: MouseButton | str = MouseButton.LEFT,
             duration: float = 0.0) -> None:
        """拖拽到指定位置"""
        if isinstance(button, str):
            button = MouseButton(button)

        self.press(button)
        time.sleep(0.05)
        self.move(x, y, duration)
        time.sleep(0.05)
        self.release(button)

    def drag_rel(self, dx: int, dy: int, button: MouseButton | str = MouseButton.LEFT,
                 duration: float = 0.0) -> None:
        """相对拖拽"""
        current = self.position()
        self.drag(current.x + dx, current.y + dy, button, duration)

    # ============ 滚动 ============

    def scroll(self, dx: int = 0, dy: int = 0) -> None:
        """滚动鼠标滚轮

        Args:
            dx: 横向滚动量（正值向右，负值向左）
            dy: 纵向滚动量（正值向上，负值向下）
        """
        self._backend.mouse_scroll(dx, dy)

    def scroll_up(self, clicks: int = 3) -> None:
        """向上滚动"""
        self.scroll(dy=clicks)

    def scroll_down(self, clicks: int = 3) -> None:
        """向下滚动"""
        self.scroll(dy=-clicks)

    def scroll_left(self, clicks: int = 3) -> None:
        """向左滚动"""
        self.scroll(dx=-clicks)

    def scroll_right(self, clicks: int = 3) -> None:
        """向右滚动"""
        self.scroll(dx=clicks)

    # ============ 高级功能 ============

    def smooth_move(self, x: int, y: int, duration: float = 0.5) -> None:
        """平滑移动（贝塞尔曲线）"""
        def ease_in_out_cubic(t: float) -> float:
            if t < 0.5:
                return 4 * t * t * t
            else:
                return 1 - pow(-2 * t + 2, 3) / 2

        self.move(x, y, duration, easing=ease_in_out_cubic)

# 导出单例
mouse = Mouse()
```

### 4.2 键盘模块（core/keyboard.py）

```python
import time
from ..backend import get_backend
from .types import Key

class Keyboard:
    """键盘操作统一接口"""

    def __init__(self):
        self._backend = get_backend()

    # ============ 基础操作 ============

    def press(self, key: Key | str) -> None:
        """按下按键"""
        self._backend.key_press(key)

    def release(self, key: Key | str) -> None:
        """释放按键"""
        self._backend.key_release(key)

    def tap(self, key: Key | str, times: int = 1, interval: float = 0.05) -> None:
        """点击按键（按下+释放）

        Args:
            key: 按键
            times: 点击次数
            interval: 多次点击的间隔
        """
        for i in range(times):
            self.press(key)
            time.sleep(0.01)
            self.release(key)
            if i < times - 1:
                time.sleep(interval)

    def is_pressed(self, key: Key | str) -> bool:
        """检查按键是否按下"""
        return self._backend.key_is_pressed(key)

    # ============ 文本输入 ============

    def write(self, text: str, interval: float = 0.0) -> None:
        """输入文本

        Args:
            text: 要输入的文本（支持Unicode）
            interval: 字符间隔时间
        """
        if interval <= 0:
            self._backend.key_type_unicode(text)
        else:
            for char in text:
                self._backend.key_type_unicode(char)
                time.sleep(interval)

    # ============ 组合键 ============

    def hotkey(self, *keys: Key | str, interval: float = 0.01) -> None:
        """按组合键

        按顺序按下所有键，然后逆序释放
        例如: hotkey('ctrl', 'shift', 's')
        """
        # 按下所有键
        for key in keys:
            self.press(key)
            if interval > 0:
                time.sleep(interval)

        # 短暂等待
        time.sleep(0.02)

        # 逆序释放
        for key in reversed(keys):
            self.release(key)
            if interval > 0:
                time.sleep(interval)

    def press_and_hold(self, key: Key | str, duration: float) -> None:
        """按住按键一段时间"""
        self.press(key)
        time.sleep(duration)
        self.release(key)

    # ============ 修饰键状态 ============

    def get_modifiers(self) -> set[Key]:
        """获取当前按下的修饰键"""
        modifiers = set()
        modifier_keys = [
            Key.SHIFT, Key.CTRL, Key.ALT,
            Key.CMD, Key.WIN, Key.SUPER
        ]
        for key in modifier_keys:
            try:
                if self.is_pressed(key):
                    modifiers.add(key)
            except:
                pass
        return modifiers

    # ============ 键盘布局 ============

    def get_layout(self) -> str:
        """获取当前键盘布局"""
        return self._backend.get_keyboard_layout()

# 导出单例
keyboard = Keyboard()
```

### 4.3 显示器模块（core/display.py）

```python
from ..backend import get_backend
from .types import DisplayInfo, Point, Rect

class Display:
    """显示器管理接口"""

    def __init__(self):
        self._backend = get_backend()

    # ============ 显示器信息 ============

    def all(self) -> list[DisplayInfo]:
        """获取所有显示器"""
        return self._backend.get_displays()

    def primary(self) -> DisplayInfo:
        """获取主显示器"""
        return self._backend.get_primary_display()

    def count(self) -> int:
        """获取显示器数量"""
        return len(self.all())

    def at_point(self, x: int, y: int) -> DisplayInfo | None:
        """获取指定坐标所在的显示器"""
        point = Point(x, y)
        for display in self.all():
            if display.bounds.contains(point):
                return display
        return None

    # ============ 虚拟屏幕 ============

    def virtual_rect(self) -> Rect:
        """获取虚拟屏幕矩形（所有显示器的总区域）"""
        return self._backend.get_virtual_screen_rect()

    # ============ 坐标转换 ============

    def to_physical(self, point: Point, display: DisplayInfo | None = None) -> Point:
        """逻辑坐标转物理坐标（考虑DPI缩放）"""
        if display is None:
            display = self.at_point(point.x, point.y)
            if display is None:
                display = self.primary()

        # 计算相对于显示器的坐标
        rel_x = point.x - display.bounds.x
        rel_y = point.y - display.bounds.y

        # 应用缩放
        phys_x = int(rel_x * display.scale)
        phys_y = int(rel_y * display.scale)

        return Point(
            display.bounds.x + phys_x,
            display.bounds.y + phys_y
        )

    def from_physical(self, point: Point, display: DisplayInfo | None = None) -> Point:
        """物理坐标转逻辑坐标"""
        if display is None:
            # 需要找到包含该物理坐标的显示器
            for d in self.all():
                phys_bounds = Rect(
                    d.bounds.x,
                    d.bounds.y,
                    int(d.bounds.width * d.scale),
                    int(d.bounds.height * d.scale)
                )
                if phys_bounds.contains(point):
                    display = d
                    break
            if display is None:
                display = self.primary()

        # 计算相对于显示器的物理坐标
        rel_x = point.x - display.bounds.x
        rel_y = point.y - display.bounds.y

        # 应用逆缩放
        log_x = int(rel_x / display.scale)
        log_y = int(rel_y / display.scale)

        return Point(
            display.bounds.x + log_x,
            display.bounds.y + log_y
        )

# 导出单例
display = Display()
```

### 4.4 窗口模块（core/window.py）

```python
from typing import Callable
from ..backend import get_backend
from .types import WindowInfo, WindowState, Rect

class Window:
    """窗口管理接口"""

    def __init__(self):
        self._backend = get_backend()

    # ============ 窗口查询 ============

    def list(self, visible_only: bool = True) -> list[WindowInfo]:
        """列出所有窗口"""
        return self._backend.list_windows(visible_only)

    def active(self) -> WindowInfo | None:
        """获取当前激活窗口"""
        return self._backend.get_active_window()

    def find(self, title: str | None = None,
             class_name: str | None = None,
             pid: int | None = None,
             predicate: Callable[[WindowInfo], bool] | None = None) -> list[WindowInfo]:
        """查找窗口

        Args:
            title: 标题包含此字符串
            class_name: 类名包含此字符串
            pid: 进程ID匹配
            predicate: 自定义过滤函数
        """
        windows = self.list()
        results = []

        for win in windows:
            if title and title.lower() not in win.title.lower():
                continue
            if class_name and class_name.lower() not in win.class_name.lower():
                continue
            if pid is not None and win.pid != pid:
                continue
            if predicate and not predicate(win):
                continue
            results.append(win)

        return results

    def at_point(self, x: int, y: int) -> WindowInfo | None:
        """获取指定坐标处的窗口"""
        return self._backend.get_window_at(x, y)

    # ============ 窗口操作 ============

    def focus(self, window: WindowInfo | int) -> None:
        """激活/聚焦窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.focus_window(handle)

    def close(self, window: WindowInfo | int) -> None:
        """关闭窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.close_window(handle)

    # ============ 位置和大小 ============

    def position(self, window: WindowInfo | int) -> tuple[int, int]:
        """获取窗口位置"""
        # 通过重新获取窗口信息
        if isinstance(window, WindowInfo):
            return (window.rect.x, window.rect.y)
        # 需要重新查询
        windows = self.list(visible_only=False)
        for w in windows:
            if w.handle == window:
                return (w.rect.x, w.rect.y)
        raise ValueError("Window not found")

    def size(self, window: WindowInfo | int) -> tuple[int, int]:
        """获取窗口大小"""
        if isinstance(window, WindowInfo):
            return (window.rect.width, window.rect.height)
        windows = self.list(visible_only=False)
        for w in windows:
            if w.handle == window:
                return (w.rect.width, w.rect.height)
        raise ValueError("Window not found")

    def move(self, window: WindowInfo | int, x: int, y: int) -> None:
        """移动窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.move_window(handle, x, y)

    def resize(self, window: WindowInfo | int, width: int, height: int) -> None:
        """调整窗口大小"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.resize_window(handle, width, height)

    def move_resize(self, window: WindowInfo | int, x: int, y: int,
                   width: int, height: int) -> None:
        """同时移动和调整大小"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.move_window(handle, x, y)
        self._backend.resize_window(handle, width, height)

    def set_rect(self, window: WindowInfo | int, rect: Rect) -> None:
        """设置窗口矩形"""
        self.move_resize(window, rect.x, rect.y, rect.width, rect.height)

    # ============ 窗口状态 ============

    def minimize(self, window: WindowInfo | int) -> None:
        """最小化窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.MINIMIZED)

    def maximize(self, window: WindowInfo | int) -> None:
        """最大化窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.MAXIMIZED)

    def restore(self, window: WindowInfo | int) -> None:
        """恢复窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.NORMAL)

    def fullscreen(self, window: WindowInfo | int) -> None:
        """全屏窗口"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_state(handle, WindowState.FULLSCREEN)

    def get_state(self, window: WindowInfo | int) -> WindowState:
        """获取窗口状态"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        return self._backend.get_window_state(handle)

    # ============ 高级属性 ============

    def set_opacity(self, window: WindowInfo | int, opacity: float) -> None:
        """设置窗口不透明度 (0.0-1.0)"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_opacity(handle, max(0.0, min(1.0, opacity)))

    def set_always_on_top(self, window: WindowInfo | int, enabled: bool) -> None:
        """设置窗口置顶"""
        handle = window.handle if isinstance(window, WindowInfo) else window
        self._backend.set_window_always_on_top(handle, enabled)

# 导出单例
window = Window()
```

### 4.5 剪贴板模块（core/clipboard.py）

```python
from ..backend import get_backend

class Clipboard:
    """剪贴板操作接口"""

    def __init__(self):
        self._backend = get_backend()

    def get_text(self) -> str:
        """获取剪贴板文本"""
        return self._backend.clipboard_get_text()

    def set_text(self, text: str) -> None:
        """设置剪贴板文本"""
        self._backend.clipboard_set_text(text)

    def clear(self) -> None:
        """清空剪贴板"""
        self._backend.clipboard_clear()

    def has_text(self) -> bool:
        """检查剪贴板是否有文本"""
        return self._backend.clipboard_has_text()

# 导出单例
clipboard = Clipboard()
```

---

## 5. 宏系统设计

### 5.1 宏操作（core/macro.py）

```python
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable
from .types import *

class MacroContext:
    """宏执行上下文"""

    def __init__(self, macro: "Macro"):
        self.macro = macro
        self.variables: dict[str, Any] = {}
        self.should_stop = False

    def set(self, name: str, value: Any) -> None:
        """设置变量"""
        self.variables[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        """获取变量"""
        return self.variables.get(name, default)

    def stop(self) -> None:
        """停止宏执行"""
        self.should_stop = True

class Action(ABC):
    """动作基类"""

    @abstractmethod
    def execute(self, ctx: MacroContext) -> None:
        """执行动作"""
        pass

# ============ 鼠标动作 ============

@dataclass
class MouseMove(Action):
    x: int
    y: int
    duration: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse
        mouse.move(self.x, self.y, self.duration)

@dataclass
class MouseClick(Action):
    button: str = "left"
    clicks: int = 1
    interval: float = 0.1

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse
        mouse.click(button=self.button, clicks=self.clicks, interval=self.interval)

@dataclass
class MouseDrag(Action):
    x: int
    y: int
    button: str = "left"
    duration: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse
        mouse.drag(self.x, self.y, button=self.button, duration=self.duration)

@dataclass
class MouseScroll(Action):
    dx: int = 0
    dy: int = 0

    def execute(self, ctx: MacroContext) -> None:
        from .mouse import mouse
        mouse.scroll(self.dx, self.dy)

# ============ 键盘动作 ============

@dataclass
class KeyPress(Action):
    key: Key | str

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard
        keyboard.press(self.key)

@dataclass
class KeyRelease(Action):
    key: Key | str

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard
        keyboard.release(self.key)

@dataclass
class KeyTap(Action):
    key: Key | str
    times: int = 1
    interval: float = 0.05

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard
        keyboard.tap(self.key, self.times, self.interval)

@dataclass
class KeyWrite(Action):
    text: str
    interval: float = 0.0

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard
        keyboard.write(self.text, self.interval)

@dataclass
class KeyHotkey(Action):
    keys: tuple[Key | str, ...]

    def execute(self, ctx: MacroContext) -> None:
        from .keyboard import keyboard
        keyboard.hotkey(*self.keys)

# ============ 控制流动作 ============

@dataclass
class Wait(Action):
    seconds: float

    def execute(self, ctx: MacroContext) -> None:
        time.sleep(self.seconds)

@dataclass
class Repeat(Action):
    actions: list[Action]
    times: int

    def execute(self, ctx: MacroContext) -> None:
        for _ in range(self.times):
            if ctx.should_stop:
                break
            for action in self.actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break

@dataclass
class Condition(Action):
    condition: Callable[[MacroContext], bool]
    then_actions: list[Action]
    else_actions: list[Action] | None = None

    def execute(self, ctx: MacroContext) -> None:
        if self.condition(ctx):
            for action in self.then_actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break
        elif self.else_actions:
            for action in self.else_actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break

@dataclass
class Loop(Action):
    actions: list[Action]
    condition: Callable[[MacroContext], bool] | None = None
    max_iterations: int | None = None

    def execute(self, ctx: MacroContext) -> None:
        iterations = 0
        while True:
            if ctx.should_stop:
                break
            if self.condition and not self.condition(ctx):
                break
            if self.max_iterations and iterations >= self.max_iterations:
                break

            for action in self.actions:
                action.execute(ctx)
                if ctx.should_stop:
                    break

            iterations += 1

# ============ 宏类 ============

class Macro:
    """宏 - 动作序列"""

    def __init__(self, name: str | None = None):
        self.name = name or "unnamed"
        self.actions: list[Action] = []

    def add(self, action: Action) -> "Macro":
        """添加动作（链式调用）"""
        self.actions.append(action)
        return self

    def wait(self, seconds: float) -> "Macro":
        """添加等待（快捷方法）"""
        return self.add(Wait(seconds))

    def run(self, **variables) -> None:
        """执行宏

        Args:
            **variables: 初始变量
        """
        ctx = MacroContext(self)
        ctx.variables.update(variables)

        for action in self.actions:
            if ctx.should_stop:
                break
            action.execute(ctx)

    def repeat(self, times: int) -> None:
        """重复执行宏"""
        for _ in range(times):
            self.run()

# ============ 便捷函数 ============

def macro(name: str | None = None) -> Macro:
    """创建宏"""
    return Macro(name)
```

---

## 6. 事件监听（core/events.py）

```python
from typing import Callable
from ..backend import get_backend
from .types import MouseEvent, KeyboardEvent

class Events:
    """全局事件监听"""

    def __init__(self):
        self._backend = get_backend()
        self._hooks: dict[Any, str] = {}  # hook_handle -> type

    def on_mouse(self, callback: Callable[[MouseEvent], bool]) -> Any:
        """注册鼠标事件监听

        Args:
            callback: 回调函数，返回False可阻止事件传递

        Returns:
            hook句柄，用于取消监听
        """
        handle = self._backend.hook_mouse(callback)
        self._hooks[handle] = "mouse"
        return handle

    def on_keyboard(self, callback: Callable[[KeyboardEvent], bool]) -> Any:
        """注册键盘事件监听

        Args:
            callback: 回调函数，返回False可阻止事件传递

        Returns:
            hook句柄，用于取消监听
        """
        handle = self._backend.hook_keyboard(callback)
        self._hooks[handle] = "keyboard"
        return handle

    def unhook(self, handle: Any) -> None:
        """取消事件监听"""
        if handle in self._hooks:
            self._backend.unhook(handle)
            del self._hooks[handle]

    def unhook_all(self) -> None:
        """取消所有事件监听"""
        for handle in list(self._hooks.keys()):
            self.unhook(handle)

# 导出单例
events = Events()
```

---

## 7. 异常设计（core/errors.py）

```python
class GuiGuiGuiError(Exception):
    """GuiGuiGui 基础异常"""
    pass

class BackendNotAvailableError(GuiGuiGuiError):
    """后端不可用"""
    pass

class PermissionDeniedError(GuiGuiGuiError):
    """权限不足"""
    def __init__(self, feature: str, platform_hint: str = ""):
        self.feature = feature
        self.platform_hint = platform_hint
        super().__init__(
            f"Permission denied for {feature}. {platform_hint}"
        )

class BackendCapabilityError(GuiGuiGuiError):
    """后端不支持某功能"""
    def __init__(self, feature: str, backend: str):
        self.feature = feature
        self.backend = backend
        super().__init__(
            f"Feature '{feature}' is not supported on {backend} backend"
        )

class WindowNotFoundError(GuiGuiGuiError):
    """窗口未找到"""
    pass

class DisplayNotFoundError(GuiGuiGuiError):
    """显示器未找到"""
    pass
```

---

## 8. 平台实现要点

### 8.1 Windows (Win32 API)

**核心技术：**
- `SendInput` - 输入模拟
- `EnumWindows` - 窗口枚举
- `SetWindowPos` - 窗口操作
- `EnumDisplayMonitors` - 多显示器
- `SetProcessDpiAwarenessContext` - DPI感知

**关键点：**
- 使用 ctypes 避免 pywin32 依赖
- 正确处理 DPI 缩放
- 使用 `SendInput` 而非 `mouse_event`/`keybd_event`

### 8.2 macOS (Cocoa/Quartz)

**核心技术：**
- `CGEvent` - 输入模拟
- `Accessibility API` - 窗口管理
- `CGDisplay` - 显示器管理
- `NSPasteboard` - 剪贴板

**关键点：**
- 需要辅助功能权限
- 处理 Retina 屏幕缩放
- 键盘事件需要 keycode 映射

### 8.3 Linux X11

**核心技术：**
- `XTest` - 输入模拟
- `EWMH` - 窗口管理
- `XRandR` - 多显示器
- `X Selection` - 剪贴板

**关键点：**
- 使用 python-xlib
- 不同桌面环境可能有差异
- DPI 计算需要额外处理

### 8.4 Linux Wayland

**限制：**
- 安全模型限制全局输入模拟
- 窗口管理能力受限
- 需要外部工具（ydotool 等）

**策略：**
- 标注为"受限支持"
- 尽力而为，不可用时明确报错

---

## 9. 依赖管理

### 9.1 pyproject.toml

```toml
[project]
name = "guiguigui"
version = "0.1.0"
description = "Cross-platform GUI automation library"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "Your Name", email = "your@email.com" }]

dependencies = []

[project.optional-dependencies]
macos = [
    "pyobjc-core>=10.0",
    "pyobjc-framework-Quartz>=10.0",
    "pyobjc-framework-Cocoa>=10.0",
]
linux = [
    "python-xlib>=0.33",
]
windows = []  # 使用 ctypes，无额外依赖

dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "mypy>=1.0",
]

[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.10"
strict = true
```

---

## 10. 使用示例

### 10.1 基础操作

```python
from guiguigui import mouse, keyboard, display, window, clipboard

# 鼠标操作
mouse.move(500, 300)
mouse.click()
mouse.drag(700, 400, duration=0.5)
mouse.scroll_down(3)

# 键盘操作
keyboard.write("Hello, World!")
keyboard.hotkey("ctrl", "s")
keyboard.tap(Key.ENTER)

# 剪贴板
clipboard.set_text("copied text")
text = clipboard.get_text()

# 显示器信息
for d in display.all():
    print(f"{d.name}: {d.bounds.width}x{d.bounds.height} @{d.scale}x")
```

### 10.2 窗口管理

```python
from guiguigui import window, display

# 查找窗口
chrome_wins = window.find(title="Chrome")
if chrome_wins:
    win = chrome_wins[0]

    # 激活窗口
    window.focus(win)

    # 移动到第二个显示器
    displays = display.all()
    if len(displays) > 1:
        second = displays[1]
        window.move(win, second.bounds.x, second.bounds.y)
        window.maximize(win)
```

### 10.3 宏操作

```python
from guiguigui import Macro, mouse, keyboard
from guiguigui.core.macro import MouseMove, MouseClick, Wait, KeyWrite, KeyHotkey

# 定义登录宏
login = (
    Macro("auto_login")
    .add(MouseMove(300, 200, 0.2))
    .add(MouseClick())
    .add(KeyWrite("username"))
    .wait(0.1)
    .add(MouseMove(300, 250, 0.2))
    .add(MouseClick())
    .add(KeyWrite("password"))
    .add(KeyHotkey(("enter",)))
)

# 执行
login.run()

# 或者重复执行
login.repeat(3)
```

### 10.4 多显示器操作

```python
from guiguigui import mouse, display

# 在每个显示器中心点击
for disp in display.all():
    center = disp.bounds.center
    mouse.smooth_move(center.x, center.y, duration=0.5)
    mouse.click()
```

---

## 11. 实现优先级

### Phase 1: 核心基础（Week 1-2）
- [ ] 项目结构和类型定义
- [ ] Backend 抽象层
- [ ] 鼠标基础操作（移动、点击）
- [ ] 键盘基础操作（按键、文本）
- [ ] 单显示器支持
- [ ] Windows 平台基础实现

### Phase 2: 完善功能（Week 3-4）
- [ ] 窗口管理完整实现
- [ ] 多显示器支持
- [ ] DPI 缩放处理
- [ ] 剪贴板操作
- [ ] macOS 平台实现
- [ ] Linux X11 实现

### Phase 3: 高级特性（Week 5-6）
- [ ] 宏系统
- [ ] 事件监听（可选）
- [ ] 平滑移动和缓动
- [ ] Wayland 受限支持
- [ ] 完善错误处理
- [ ] 权限检查

### Phase 4: 完善和发布（Week 7-8）
- [ ] 完整测试套件
- [ ] API 文档
- [ ] 使用示例
- [ ] 性能优化
- [ ] 打包和发布

---

## 12. 非功能性需求

### 12.1 明确"不做的事"

GuiGuiGui 专注于底层 GUI 操作，以下功能**不在**范围内：

- ❌ 图像识别和模板匹配
- ❌ OCR 文字识别
- ❌ UI 元素定位（如 xpath）
- ❌ 浏览器自动化（使用 Selenium/Playwright）
- ❌ 移动端支持
- ❌ 录屏/截图

### 12.2 性能目标

- 鼠标移动延迟 < 10ms
- 键盘输入延迟 < 5ms
- 窗口枚举 < 100ms
- 内存占用 < 50MB

### 12.3 兼容性

- Python 3.10+
- macOS 11+
- Windows 10+
- Linux (主流发行版，X11 优先)

---

## 13. 测试策略

### 13.1 单元测试
- Mock Backend 测试核心逻辑
- 类型定义和工具函数

### 13.2 集成测试
- 实际平台测试（需要显示环境）
- CI/CD 中使用虚拟显示

### 13.3 平台测试
- 每个平台的特定测试
- 权限检查测试

---

## 14. 文档结构

```
docs/
├── api.md              # API 完整参考
├── quickstart.md       # 快速开始
├── platforms/
│   ├── windows.md      # Windows 特性和限制
│   ├── macos.md        # macOS 特性和限制
│   └── linux.md        # Linux 特性和限制
├── guides/
│   ├── multi_monitor.md
│   ├── window_management.md
│   └── macros.md
└── migration.md        # 从其他库迁移
```

---

## 15. 后续扩展方向

- 录制和回放宏
- 宏序列化（JSON/YAML）
- 热键注册
- 性能监控和统计
- 远程控制支持
- 插件系统

---

## 总结

GuiGuiGui 是一个精简、专注的跨平台 GUI 自动化库：

✅ **完备** - 覆盖鼠标、键盘、窗口、显示器、剪贴板
✅ **跨平台** - Windows / macOS / Linux
✅ **多屏支持** - 完整的多显示器和 DPI 处理
✅ **可扩展** - 清晰的抽象层和宏系统
✅ **极简** - 无冗余功能，依赖最小化

适用场景：GUI 自动化测试、重复任务自动化、辅助工具开发、游戏脚本等。
