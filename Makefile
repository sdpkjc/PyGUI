.PHONY: help test test-cov test-unit test-integration lint format type-check security check-all clean install install-hooks update-hooks

# 默认目标：显示帮助
help:
	@echo "GuiGuiGui 开发命令"
	@echo ""
	@echo "测试:"
	@echo "  make test           - 运行所有测试"
	@echo "  make test-cov       - 运行测试并生成覆盖率报告"
	@echo "  make test-unit      - 只运行单元测试"
	@echo "  make test-integration - 只运行集成测试"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint           - 运行代码检查（ruff）"
	@echo "  make format         - 格式化代码（ruff format）"
	@echo "  make type-check     - 类型检查（mypy）"
	@echo "  make security       - 安全扫描（bandit）"
	@echo "  make check-all      - 运行所有检查"
	@echo ""
	@echo "开发环境:"
	@echo "  make install        - 安装依赖"
	@echo "  make install-hooks  - 安装 pre-commit hooks"
	@echo "  make update-hooks   - 更新 pre-commit hooks"
	@echo "  make clean          - 清理临时文件"

# 测试命令
test:
	uv run pytest

test-cov:
	uv run pytest --cov=guiguigui --cov-report=html --cov-report=term --cov-report=xml

test-unit:
	uv run pytest tests/unit/ tests/platform/

test-integration:
	uv run pytest tests/integration/ -m integration

# 代码质量检查
lint:
	uv run ruff check guiguigui tests examples

format:
	uv run ruff format guiguigui tests examples

format-check:
	uv run ruff format --check guiguigui tests examples

type-check:
	uv run mypy guiguigui

security:
	uv run bandit -r guiguigui -c pyproject.toml

# 运行所有检查（类似CI）
check-all: lint format-check type-check security test
	@echo ""
	@echo "✅ 所有检查通过！"

# 开发环境设置
install:
	uv sync --extra dev --extra macos

install-linux:
	uv sync --extra dev --extra linux

install-hooks:
	uv run pre-commit install --install-hooks

update-hooks:
	uv run pre-commit autoupdate

# 清理命令
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	rm -rf dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# 构建和发布
build:
	uv build

publish-test:
	uv publish --token $$PYPI_TEST_TOKEN --publish-url https://test.pypi.org/legacy/

publish:
	@echo "警告：即将发布到 PyPI！"
	@read -p "确定要继续吗？(y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv publish --token $$PYPI_TOKEN; \
	fi

# 开发服务器（如果有web界面）
dev:
	@echo "guiguigui 是一个库，没有开发服务器"

# 查看覆盖率报告
show-coverage:
	@if [ -f htmlcov/index.html ]; then \
		open htmlcov/index.html || xdg-open htmlcov/index.html || start htmlcov/index.html; \
	else \
		echo "请先运行 'make test-cov' 生成覆盖率报告"; \
	fi
