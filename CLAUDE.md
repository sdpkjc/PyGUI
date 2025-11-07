# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyGUI is a minimalist cross-platform GUI automation library that provides low-level control over mouse, keyboard, windows, displays, and clipboard. It deliberately excludes image matching, OCR, and other high-level automation features, focusing purely on direct GUI operations.

**Key principle**: Only do input control, window management, display management, clipboard, and event hooks. Do NOT add image recognition, OCR, or business logic features.

## Development Commands

### Package Management (uv)

```bash
# Install dependencies (platform-specific)
uv sync --extra dev --extra macos    # macOS development
uv sync --extra dev --extra linux    # Linux development
uv sync --extra dev                  # Windows development

# Run commands in the virtual environment
uv run <command>
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_basic.py

# Run with coverage
uv run pytest --cov=pygui --cov-report=html
```

### Code Quality

```bash
# Lint and format (recommended before commit)
uv run ruff check pygui
uv run ruff format pygui

# Type checking
uv run mypy pygui

# Run all pre-commit checks
uv run pre-commit run --all-files
```

Pre-commit hooks run automatically on `git commit` and will check:
- Trailing whitespace
- YAML/TOML syntax
- Ruff linting and formatting
- Mypy type checking

### Running Examples

```bash
uv run python examples/basic_operations.py
uv run python examples/multi_monitor.py
uv run python examples/macro_example.py
```

## Architecture

### Three-Layer Design

1. **Backend Layer** (`pygui/backend/`): Platform-specific implementations
   - `base.py`: Abstract `Backend` class defining 30+ methods
   - `macos.py`: Uses PyObjC (Quartz/Cocoa APIs)
   - `x11.py`: Uses python-xlib (not yet implemented)
   - `win32.py`: Uses ctypes/pywin32 (not yet implemented)
   - `wayland.py`: Limited support (not yet implemented)

2. **Core Layer** (`pygui/core/`): Platform-agnostic API
   - `mouse.py`, `keyboard.py`, `window.py`, `display.py`, `clipboard.py`: User-facing APIs
   - `types.py`: Shared data structures (Point, Rect, WindowInfo, DisplayInfo, etc.)
   - `macro.py`: Action-based macro system with DSL
   - `errors.py`: Exception hierarchy

3. **Entry Point** (`pygui/__init__.py`): Exports singleton objects
   - `mouse`, `keyboard`, `window`, `display`, `clipboard`, `events`

### Backend Loading

The backend is loaded lazily on first use via `backend.get_backend()`:
- Detects platform via `sys.platform`
- Linux: Checks for Wayland (via environment vars) and falls back to X11
- Returns singleton backend instance

### Coordinate System

**Critical**: All coordinates use a unified logical coordinate system:
- Primary display's top-left is (0, 0)
- Multiple displays form a virtual desktop
- `display.to_physical()` / `display.from_physical()` handle DPI scaling
- macOS: Scale factor (1.0, 2.0 for Retina)
- Windows: GetDpiForMonitor
- Linux: RandR extension

### Macro System

Macros are composed of `Action` objects (MouseMove, MouseClick, KeyPress, Wait, etc.):
- Actions have an `execute(ctx: MacroContext)` method
- Supports control flow: Repeat, Condition, Loop
- Chainable builder pattern: `Macro().add(...).wait(0.1).add(...)`

## Code Style

### Type Annotations

**IMPORTANT**: All modules must include `from __future__ import annotations` at the top to avoid runtime issues with type hints (especially when method names shadow built-in types like `list` in `Window.list()`).

### Ruff Configuration

- Line length: 100
- Target: Python 3.10+
- Enabled rules: E, W, F, I, B, C4, UP
- Ignored: E501 (line too long), E741 (ambiguous names I, O are intentional in Key enum)

### Mypy Configuration

- Mode: Moderate (not strict)
- Tests and examples are excluded from type checking
- `pygui.core.window` has `valid-type` error disabled due to method name collision

## Platform-Specific Notes

### macOS Implementation

- **Permissions**: Requires Accessibility permission for keyboard/mouse/window control
- **APIs**:
  - Mouse/Keyboard: CGEvent (Quartz)
  - Windows: Accessibility API (AXUIElement) - limited capabilities
  - Displays: CGDisplay, NSScreen
  - Clipboard: NSPasteboard
- **Limitations**: Window move/resize/state operations raise `BackendCapabilityError` due to macOS restrictions
- **Display API**: `CGGetActiveDisplayList` returns `(error, display_list, count)` tuple

### Linux (X11)

- Use python-xlib for X11 protocol
- XTest extension for input simulation
- EWMH for window management
- RandR for multi-monitor support

### Windows

- Use ctypes (preferred) or pywin32
- SendInput for input simulation
- Win32 API (User32.dll) for window management
- No extra dependencies needed

### Wayland

- Mark as "limited support" - security model restricts global automation
- May require external tools (ydotool, wtype)
- Different desktop environments have different capabilities

## Adding New Features

### Adding a New Backend

1. Create `pygui/backend/<platform>.py`
2. Subclass `Backend` from `base.py`
3. Implement all abstract methods
4. Add platform detection in `backend/__init__.py._load_backend()`
5. Add optional dependencies to `pyproject.toml`

### Adding a New Core Operation

1. Add method to `Backend` base class
2. Implement in all platform backends
3. Add user-facing API to appropriate core module (mouse/keyboard/etc.)
4. Update type hints in `core/types.py` if needed

### Adding a New Macro Action

1. Create dataclass subclassing `Action` in `core/macro.py`
2. Implement `execute(ctx: MacroContext)` method
3. Import relevant singletons inside `execute()` to avoid circular imports

## Testing Strategy

- **Unit tests**: Test data structures and utility functions (no backend needed)
- **Integration tests**: Test actual GUI operations (requires display/accessibility permissions)
- **Platform tests**: Platform-specific behavior validation

Current test coverage is minimal - focus on `types.py` (Point, Rect, Size).

## Common Issues

### "TypeError: 'function' object is not subscriptable"

Add `from __future__ import annotations` at the top of the module. This is required when using type hints with generics (like `list[WindowInfo]`) in Python 3.10.

### Accessibility Permissions (macOS)

Check permissions with `backend.check_permissions()`. If denied, raise `PermissionDeniedError` with instructions to enable in System Preferences.

### Platform Feature Not Supported

Raise `BackendCapabilityError("feature_name", "platform")` rather than silently failing or returning None. This makes limitations explicit.

## Project Goals and Non-Goals

### Goals
- Reliable, low-level GUI control primitives
- Consistent API across platforms
- Good DPI/multi-monitor handling
- Minimal dependencies

### Non-Goals
- Image recognition or template matching
- OCR or text recognition
- Element-level UI automation (like Selenium)
- Screen recording or capture
- Any AI/ML features
