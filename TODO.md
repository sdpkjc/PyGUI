# PyGUI Development TODO List

这是 PyGUI 项目的开发计划，按优先级和类别组织。

## ⚠️ 当前状态

- ✅ macOS 基础功能（鼠标、键盘、显示器、剪贴板）
- ❌ Windows 后端（未实现）
- ❌ Linux 后端（未实现）
- ⚠️ macOS 窗口管理（功能受限）
- ❌ 事件钩子（所有平台都未实现）
- ⚠️ 测试覆盖率极低（仅类型测试）

---

## 🚀 Phase 1: 核心功能完善（高优先级）

### 1.1 Backend 实现

- [ ] **Backend: Implement Windows (win32.py) backend with ctypes/pywin32**
  - 使用 ctypes 访问 User32.dll
  - 实现 SendInput 用于鼠标/键盘
  - 实现窗口管理（EnumWindows, SetForegroundWindow 等）
  - 实现多显示器支持（EnumDisplayMonitors）
  - 参考：DESIGN.md 中的 Windows 实现要点

- [ ] **Backend: Implement Linux X11 (x11.py) backend with python-xlib**
  - 使用 python-xlib 连接 X11
  - 使用 XTest 扩展模拟输入
  - 使用 EWMH 进行窗口管理
  - 使用 RandR 处理多显示器
  - 参考：DESIGN.md 中的 Linux X11 实现要点

- [ ] **Backend: Implement Linux Wayland (wayland.py) backend with limited support**
  - 明确标注为"受限支持"
  - 封装 ydotool/wtype 等外部工具
  - 在工具不可用时抛出 BackendCapabilityError
  - 文档说明限制

### 1.2 macOS 功能完善

- [ ] **macOS: Implement window management operations using Accessibility API**
  - 实现 move_window (AXSetPosition)
  - 实现 resize_window (AXSetSize)
  - 实现 close_window (AXPerformAction with AXPress)
  - 实现 set_window_state (最小化/最大化)
  - 实现 set_window_opacity
  - 实现 set_window_always_on_top
  - 需要处理权限检查

- [ ] **macOS: Implement event hooks (mouse and keyboard global listeners)**
  - 使用 CGEventTap 实现全局钩子
  - 实现 hook_mouse 方法
  - 实现 hook_keyboard 方法
  - 处理事件过滤和回调
  - 需要辅助功能权限

---

## 🧪 Phase 2: 测试体系建设（高优先级）

### 2.1 单元测试

- [ ] **Tests: Add comprehensive unit tests for core modules**
  - `tests/unit/test_mouse.py` - 测试鼠标 API 逻辑
  - `tests/unit/test_keyboard.py` - 测���键盘 API 逻辑
  - `tests/unit/test_display.py` - 测试显示器坐标转换
  - `tests/unit/test_window.py` - 测试窗口查找逻辑
  - `tests/unit/test_macro.py` - 测试宏系统
  - `tests/unit/test_clipboard.py` - 测试剪贴板 API
  - 使用 Mock Backend 避免实际 GUI 操作

### 2.2 集成测试

- [ ] **Tests: Add integration tests for actual GUI operations**
  - `tests/integration/test_mouse_operations.py`
  - `tests/integration/test_keyboard_operations.py`
  - `tests/integration/test_window_operations.py`
  - `tests/integration/test_multi_monitor.py`
  - 需要实际的显示环境
  - CI 中使用虚拟显示（Xvfb）

### 2.3 平台测试

- [ ] **Tests: Add platform-specific tests for each backend**
  - `tests/platform/test_macos.py`
  - `tests/platform/test_windows.py`
  - `tests/platform/test_linux_x11.py`
  - `tests/platform/test_linux_wayland.py`
  - 测试平台特定行为和限制

---

## 📚 Phase 3: 示例和文档（中优先级）

### 3.1 示例程序

- [ ] **Examples: Create window_management.py example**
  - 演示窗口查找、激活、移动、调整大小
  - 演示多窗口操作
  - 演示窗口状态管理

- [ ] **Examples: Create event_hooks.py example**
  - 演示鼠标/键盘事件监听
  - 演示录制宏的基本流程
  - 演示热键注册

- [ ] **Examples: Create advanced_macro.py**
  - 演示 Repeat、Condition、Loop 使用
  - 演示参数化宏
  - 演示宏的保存/加载

### 3.2 API 文档

- [ ] **Docs: Create docs/ directory with API documentation**
  - `docs/api/mouse.md`
  - `docs/api/keyboard.md`
  - `docs/api/window.md`
  - `docs/api/display.md`
  - `docs/api/clipboard.md`
  - `docs/api/macro.md`
  - `docs/api/events.md`

- [ ] **Docs: Create platform_notes.md with detailed platform limitations**
  - macOS 权限要求和配置
  - macOS 窗口管理限制
  - Windows 无需额外依赖
  - Linux X11 vs Wayland 差异
  - 各平台的已知问题和解决方案

- [ ] **Docs: Create migration.md for users migrating from other libraries**
  - 从 pyautogui 迁移指南
  - 从 pynput 迁移指南
  - 从 pywinauto 迁移指南
  - API 对比表

---

## 🔧 Phase 4: 工具和辅助（中优先级）

### 4.1 Util 模块

- [ ] **Util: Implement platform.py for platform detection utilities**
  - `is_macos()`, `is_windows()`, `is_linux()`
  - `is_x11()`, `is_wayland()`
  - `get_platform_info()` 返回详细信息
  - `check_dependencies()` 检查平台依赖

- [ ] **Util: Implement dpi.py for DPI conversion helpers**
  - `get_dpi_scale(display)` 获取 DPI 缩放
  - `logical_to_physical(point, display)` 坐标转换
  - `physical_to_logical(point, display)` 坐标转换
  - 处理不同 DPI 显示器之间的移动

- [ ] **Util: Implement timing.py with retry/wait utilities**
  - `wait_for(condition, timeout, interval)` 等待条件
  - `retry(func, max_attempts, delay)` 重试机制
  - `rate_limit(calls_per_second)` 速率限制装饰器
  - 用于处理异步 GUI 操作

---

## 🔄 Phase 5: CI/CD 和自动化（中优先级）

### 5.1 GitHub Actions

- [ ] **CI/CD: Setup GitHub Actions for multi-platform testing**
  - `.github/workflows/test.yml`
  - 在 macOS, Windows, Linux (Ubuntu) 上运行测试
  - 使用矩阵策略测试 Python 3.10, 3.11, 3.12
  - Linux 使用 Xvfb 进行无头测试

- [ ] **CI/CD: Add test coverage reporting**
  - 集成 codecov 或 coveralls
  - 在 PR 中显示覆盖率变化
  - 要求最低覆盖率（如 80%）

- [ ] **CI/CD: Add automatic release workflow**
  - `.github/workflows/release.yml`
  - 在 git tag 时自动构建和发布到 PyPI
  - 生成 GitHub Release notes
  - 构建 wheel 和 sdist

---

## ✨ Phase 6: 高级特性（低优先级）

### 6.1 事件钩子相关

- [ ] **Windows: Implement event hooks using SetWindowsHookEx**
  - 低级钩子 WH_MOUSE_LL / WH_KEYBOARD_LL
  - 处理消息循环
  - 支持事件阻止

- [ ] **Linux: Implement event hooks for X11**
  - 使用 XRecordExtension 记录输入
  - 或使用 XGrabKey/XGrabButton
  - 处理事件分发

- [ ] **Features: Implement macro recording from event hooks**
  - `MacroRecorder` 类
  - `start()`, `stop()`, `pause()`, `resume()` 方法
  - 自动生成 Action 列表
  - 过滤噪声事件

### 6.2 宏系统增强

- [ ] **Features: Implement macro serialization to JSON/YAML**
  - Action 到 dict 的序列化
  - dict 到 Action 的反序列化
  - `Macro.save(path)` 和 `Macro.load(path)`
  - 支持参数化和变量

### 6.3 剪贴板增强

- [ ] **Features: Add clipboard support for images**
  - macOS: NSPasteboard with NSImage
  - Windows: CF_DIB / CF_DIBV5
  - Linux: image/png MIME type
  - 返回 PIL Image 或 bytes

- [ ] **Features: Add clipboard support for files**
  - macOS: NSFilenamesPboardType
  - Windows: CF_HDROP
  - Linux: text/uri-list
  - `clipboard.get_files()` 返回路径列表

---

## ⚡ Phase 7: 性能和优化（低优先级）

### 7.1 性能优化

- [ ] **Performance: Benchmark and optimize critical paths**
  - 使用 `pytest-benchmark` 测试性能
  - 优化坐标转换（避免重复计算）
  - 优化窗口查询（减少系统调用）
  - 记录性能基准

- [ ] **Performance: Add caching for display/window queries**
  - 缓存显示器信息（DPI 很少变化）
  - 缓存窗口列表（带超时）
  - 提供 `refresh()` 方法手动刷新
  - 配置缓存策略

---

## 🛡️ Phase 8: 错误处理和用户体验（低优先级）

### 8.1 错误处理改进

- [ ] **Error Handling: Improve error messages with actionable suggestions**
  - 检测到权限不足时给出配置指引
  - 检测到缺少依赖时给出安装命令
  - 提供错误码和文档链接

- [ ] **Error Handling: Add permission checking and user guidance**
  - 启动时检查权限（可选）
  - `check_permissions()` 返回详细状态
  - 提供权限请求对话框（macOS）
  - 文档说明权限配置步骤

---

## 📦 Phase 9: 打包和发布（低优先级）

### 9.1 包管理

- [ ] **Packaging: Publish to PyPI**
  - 完善 `pyproject.toml` metadata
  - 添加 long_description
  - 配置 classifiers 和 keywords
  - 创建 PyPI 账号和 token
  - 首次发布 0.1.0

- [ ] **Packaging: Create conda package**
  - 创建 conda-forge feedstock
  - 配置 meta.yaml
  - 处理平台特定依赖
  - 提交到 conda-forge

### 9.2 开发者体验

- [ ] **Documentation: Add type stubs for better IDE support**
  - 生成 `.pyi` stub 文件
  - 包含在包中（py.typed）
  - 确保 IDE 自动补全正常

- [ ] **Documentation: Create tutorial series**
  - 入门教程：5 分钟快速上手
  - 进阶教程：多显示器处理
  - 进阶教程：宏系统深入
  - 进阶教程：跨平台兼容性
  - 实战案例：自动化测试
  - 实战案例：游戏脚本
  - 实战案例：办公自动化

---

## 📊 进度统计

- **总任务数**: 35
- **已完成**: 1
- **进行中**: 0
- **待完成**: 34
- **完成率**: 2.9%

---

## 🎯 里程碑

### v0.2.0 - 跨平台基础版
- [x] macOS 基础实现
- [ ] Windows 基础实现
- [ ] Linux X11 基础实现
- [ ] 基础测试覆盖（>50%）

### v0.3.0 - 功能完善版
- [ ] 事件钩子实现
- [ ] 宏录制功能
- [ ] 完整测试覆盖（>80%）
- [ ] 完整文档

### v0.4.0 - 增强版
- [ ] 剪贴板图像/文件支持
- [ ] 性能优化
- [ ] CI/CD 完善

### v1.0.0 - 稳定版
- [ ] 所有平台完整测试通过
- [ ] 完整文档和示例
- [ ] 发布到 PyPI
- [ ] 社区反馈处理

---

## 📝 开发规范

### 代码要求
- 所有模块必须包含 `from __future__ import annotations`
- 使用 ruff 进行代码检查和格式化
- 使用 mypy 进行类型检查
- 提交前运行 `uv run pre-commit run --all-files`

### 测试要求
- 新功能必须包含测试
- 单元测试覆盖率 >80%
- 集成测试覆盖主要用例

### 文档要求
- 公共 API 必须有 docstring
- 复杂逻辑需要内联注释
- 示例程序需要完整注释

### 提交规范
- 遵循 Conventional Commits
- 格式: `type(scope): description`
- 类型: feat, fix, docs, test, refactor, perf, chore

---

**最后更新**: 2025-11-08
