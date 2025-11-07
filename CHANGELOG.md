# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive unit test suite (71 tests)
- Integration tests for GUI operations
- GitHub Actions CI/CD (tests, linting, PyPI publishing)
- Mock backend for testing
- Test coverage reporting
- Complete documentation (DESIGN.md, CLAUDE.md, TODO.md, TESTING.md, RELEASING.md)

### Changed
- README now in English, more concise and professional

## [0.1.0] - TBD

### Added
- Initial release
- macOS backend with PyObjC
- Core modules: mouse, keyboard, display, window, clipboard
- Macro system for automation
- Multi-monitor support
- High-DPI support
- Type annotations throughout
- Pre-commit hooks with ruff and mypy
- Examples demonstrating all features

### Known Limitations
- Windows backend not yet implemented
- Linux (X11/Wayland) backend not yet implemented
- macOS window management has limited functionality
- Event hooks not yet implemented

[Unreleased]: https://github.com/sdpkjc/guiguigui/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sdpkjc/guiguigui/releases/tag/v0.1.0
