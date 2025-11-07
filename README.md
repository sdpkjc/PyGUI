# PyGUI

跨平台 GUI 自动化库 - 极简、完备、高效

## 特性

1. **跨平台支持** - macOS / Linux / Windows
2. **完备的 GUI 操作** - 鼠标、键盘、窗口、显示器、剪贴板
3. **多显示器支持** - 完整的多屏和高 DPI 处理
4. **强大的窗口管理** - 枚举、激活、移动、调整大小等
5. **优雅的宏系统** - 轻松定义复杂的自动化操作
6. **极简设计** - 无图像匹配、OCR 等多余功能

## 安装

### 使用 uv (推荐)

```bash
# macOS
uv sync --extra macos

# Linux
uv sync --extra linux

# Windows
uv sync

# 安装开发依赖
uv sync --extra dev --extra macos
```

### 使用 pip

```bash
pip install pygui

# macOS
pip install pygui[macos]

# Linux
pip install pygui[linux]
```

## 快速开始

### 基础操作

```python
from pygui import mouse, keyboard, display, window, clipboard

# 鼠标操作
mouse.move(500, 300)
mouse.click()
mouse.drag(700, 400, duration=0.5)
mouse.scroll_down(3)

# 键盘操作
keyboard.write("Hello, PyGUI!")
keyboard.hotkey("cmd", "s")  # macOS
keyboard.hotkey("ctrl", "s")  # Windows/Linux

# 剪贴板
clipboard.set_text("复制内容")
text = clipboard.get_text()

# 显示器信息
for d in display.all():
    print(f"{d.name}: {d.bounds.width}x{d.bounds.height} @{d.scale}x")

# 窗口管理
chrome_windows = window.find(title="Chrome")
if chrome_windows:
    window.focus(chrome_windows[0])
    window.maximize(chrome_windows[0])
```

### 宏操作

```python
from pygui import Macro
from pygui.core.macro import MouseMove, MouseClick, KeyWrite, KeyHotkey

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

login.run()
```

### 多显示器

```python
from pygui import mouse, display

displays = display.all()
if len(displays) > 1:
    second = displays[1]
    center = second.bounds.center
    mouse.smooth_move(center.x, center.y, duration=0.5)
```

## API 文档

### 鼠标 (mouse)

- `position()` - 获取鼠标位置
- `move(x, y, duration=0)` - 移动鼠标
- `click(button='left', clicks=1)` - 点击
- `double_click()` - 双击
- `drag(x, y, button='left', duration=0)` - 拖拽
- `scroll(dx=0, dy=0)` - 滚动
- `smooth_move(x, y, duration=0.5)` - 平滑移动

### 键盘 (keyboard)

- `press(key)` - 按下按键
- `release(key)` - 释放按键
- `tap(key, times=1)` - 点击按键
- `write(text, interval=0)` - 输入文本
- `hotkey(*keys)` - 组合键
- `get_layout()` - 获取键盘布局

### 显示器 (display)

- `all()` - 获取所有显示器
- `primary()` - 获取主显示器
- `at_point(x, y)` - 获取坐标所在显示器
- `virtual_rect()` - 获取虚拟屏幕矩形
- `to_physical(point)` - 逻辑坐标转物理坐标
- `from_physical(point)` - 物理坐标转逻辑坐标

### 窗口 (window)

- `list(visible_only=True)` - 列出所有窗口
- `active()` - 获取当前激活窗口
- `find(title=None, class_name=None, pid=None)` - 查找窗口
- `focus(window)` - 激活窗口
- `move(window, x, y)` - 移动窗口
- `resize(window, width, height)` - 调整大小
- `minimize/maximize/restore(window)` - 窗口状态
- `close(window)` - 关闭窗口

### 剪贴板 (clipboard)

- `get_text()` - 获取文本
- `set_text(text)` - 设置文本
- `clear()` - 清空
- `has_text()` - 检查是否有文本

## 开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/pygui.git
cd pygui

# 安装依赖（使用 uv）
uv sync --extra dev --extra macos

# 运行测试
uv run pytest

# 运行示例
uv run python examples/basic_operations.py
uv run python examples/multi_monitor.py
uv run python examples/macro_example.py

# 代码检查和格式化
uv run ruff check pygui
uv run ruff format pygui

# 类型检查
uv run mypy pygui

# 运行所有检查（pre-commit）
uv run pre-commit run --all-files
```

## 平台说明

### macOS

- 需要辅助功能权限
- 窗口管理功能有限（由于系统限制）
- 完整支持鼠标、键盘、显示器操作

### Linux

- 优先支持 X11
- Wayland 支持有限（安全限制）
- 需要安装 `python-xlib`

### Windows

- 完整支持所有功能
- 无额外依赖（使用 ctypes）

## 许可证

MIT License

## 设计文档

详见 [DESIGN.md](DESIGN.md)
