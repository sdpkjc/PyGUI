# Testing Guide

This document describes the testing infrastructure for the GuiGuiGui project.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and mock backend
├── unit/                    # Unit tests (fast, no real GUI operations)
│   ├── test_mouse.py
│   ├── test_keyboard.py
│   ├── test_display.py
│   ├── test_window.py
│   ├── test_macro.py
│   └── test_clipboard.py
└── integration/             # Integration tests (require GUI)
    ├── test_mouse_operations.py
    ├── test_keyboard_operations.py
    ├── test_display_operations.py
    └── test_clipboard_operations.py
```

## Mock Backend

Unit tests use a `MockBackend` that simulates all backend operations without requiring actual GUI operations. This allows tests to:

- Run fast
- Run in CI environments without displays
- Test edge cases that are hard to reproduce with real GUI operations
- Be deterministic and reliable

The mock backend is automatically injected via pytest fixtures in `conftest.py`.

## Running Tests

### Unit Tests

Unit tests run with a mocked backend and don't require a GUI environment:

```bash
# Run all unit tests
uv run pytest tests/unit/ -v

# Run specific test file
uv run pytest tests/unit/test_mouse.py -v

# Run specific test
uv run pytest tests/unit/test_mouse.py::TestMouse::test_position -v

# Run with coverage
uv run pytest tests/unit/ -v --cov=guiguigui --cov-report=html
```

### Integration Tests

Integration tests require a real GUI environment:

```bash
# Run integration tests (requires display)
uv run pytest tests/integration/ -v -m integration

# On Linux, use Xvfb for headless testing
Xvfb :99 -screen 0 1920x1080x24 &
DISPLAY=:99 uv run pytest tests/integration/ -v -m integration
```

### All Tests

```bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest -v --cov=guiguigui --cov-report=html --cov-report=term
```

## CI/CD

### GitHub Actions Workflows

1. **Tests** (`.github/workflows/test.yml`)
   - Runs on: Ubuntu, macOS, Windows
   - Python versions: 3.10, 3.11, 3.12
   - Runs: linting, type checking, unit tests, integration tests (macOS only)
   - Generates coverage reports
   - Uploads to Codecov

2. **Code Quality** (`.github/workflows/lint.yml`)
   - Runs on: Ubuntu only
   - Fast feedback on code quality issues
   - Runs: ruff check, ruff format, mypy

### Platform-Specific Notes

- **macOS**: Full integration tests run on GitHub Actions
- **Linux**: Uses Xvfb for headless testing
- **Windows**: Currently only unit tests (integration tests require special setup)

## Test Coverage

Current coverage (as of 2025-11-08):
- Unit tests: 71 tests covering core modules
- Integration tests: 4 test files covering actual GUI operations
- Mock backend: Full implementation of Backend abstract class

Coverage reports are generated in `htmlcov/` directory:

```bash
uv run pytest tests/unit/ --cov=guiguigui --cov-report=html
open htmlcov/index.html
```

## Writing Tests

### Unit Test Example

```python
from guiguigui.core.mouse import Mouse
from tests.conftest import MockBackend

class TestMouse:
    def test_position(self, mock_backend: MockBackend) -> None:
        mouse = Mouse()
        mock_backend._mouse_position = Point(100, 200)
        assert mouse.position() == Point(100, 200)
```

### Integration Test Example

```python
import pytest
from guiguigui import mouse

@pytest.mark.integration
class TestMouseOperations:
    def test_mouse_position(self) -> None:
        pos = mouse.position()
        assert isinstance(pos, Point)
```

## Test Markers

- `@pytest.mark.integration`: Marks tests that require actual GUI operations
- `@pytest.mark.slow`: Marks slow-running tests

Skip integration tests:
```bash
uv run pytest -v -m "not integration"
```

Run only integration tests:
```bash
uv run pytest -v -m integration
```

## Troubleshooting

### Tests fail with "ModuleNotFoundError"

Make sure dependencies are installed:
```bash
uv sync --extra dev --extra macos
```

### Integration tests fail on macOS

Grant accessibility permissions:
1. System Settings → Privacy & Security → Accessibility
2. Add Terminal or your IDE to the list

### Tests hang or timeout

Some integration tests may need more time on slower systems. Increase timeout in `pytest.ini` if needed.

## Future Improvements

1. Add platform-specific tests for Windows and Linux backends (when implemented)
2. Increase test coverage to >80%
3. Add performance benchmarks
4. Add property-based testing with Hypothesis
5. Add visual regression tests for GUI operations
