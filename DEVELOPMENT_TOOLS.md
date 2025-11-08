# 开发工具和检查建议

本文档提供了增强项目稳健性的工具和检查建议。

## 📋 目录

1. [Pre-commit Hooks 改进](#pre-commit-hooks-改进)
2. [GitHub Actions 增强](#github-actions-增强)
3. [本地开发工具](#本地开发工具)
4. [持续集成最佳实践](#持续集成最佳实践)

---

## Pre-commit Hooks 改进

### 当前配置
当前使用的hooks：
- ✅ 尾部空格清理
- ✅ 文件结尾修复
- ✅ YAML/TOML语法检查
- ✅ 大文件检查
- ✅ 合并冲突检查
- ✅ Ruff代码检查和格式化
- ✅ Mypy类型检查

### 🎯 推荐新增（优先级1 - 高价值低成本）

#### 1. **防止直接提交到主分支**
```yaml
- id: no-commit-to-branch
  args: [--branch, main, --branch, master]
```
**价值**: 防止意外提交到main，强制使用PR流程

#### 2. **检查调试语句**
```yaml
- id: debug-statements
```
**价值**: 防止提交`print()`, `pdb.set_trace()`, `breakpoint()`等调试代码

#### 3. **检查Python AST语法**
```yaml
- id: check-ast
```
**价值**: 比Python编译更快地发现语法错误

#### 4. **检查私有密钥**
```yaml
- id: detect-private-key
```
**价值**: 防止意外提交SSH私钥、API密钥等敏感信息

#### 5. **Bandit 安全扫描**
```yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.0
  hooks:
    - id: bandit
      args: [-c, pyproject.toml]
```
**价值**:
- 检测常见安全漏洞（SQL注入、硬编码密码等）
- 检测不安全的函数使用（`eval()`, `exec()`, `pickle`等）
- 对于系统级库特别重要

### 🔧 推荐新增（优先级2 - 提高代码质量）

#### 6. **文档字符串检查**
**注意**: Ruff已经包含了文档字符串检查（D系列规则），无需单独的pydocstyle。

在`pyproject.toml`中启用：
```toml
[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "D",    # pydocstyle (文档字符串)
]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

**价值**:
- Ruff比pydocstyle更快（Rust实现）
- 统一工具链，无需额外依赖
- pydocstyle已被官方标记为维护模式

#### 7. **Codespell 拼写检查**
```yaml
- repo: https://github.com/codespell-project/codespell
  rev: v2.3.0
  hooks:
    - id: codespell
```
**价值**:
- 发现注释和文档中的拼写错误
- 提高专业性

#### 8. **PyGrep Hooks - 高级检查**
```yaml
- repo: https://github.com/pre-commit/pygrep-hooks
  rev: v1.10.0
  hooks:
    - id: python-no-eval  # 禁止eval()
    - id: python-no-log-warn  # 使用logger.warning而不是warn
    - id: python-check-blanket-noqa  # 检查笼统的noqa注释
```

### ⚡ 可选增强（优先级3 - 针对特定需求）

#### 9. **依赖安全扫描**
```yaml
- repo: https://github.com/Lucas-C/pre-commit-hooks-safety
  rev: v1.3.3
  hooks:
    - id: python-safety-dependencies-check
```
**价值**: 检查依赖包的已知安全漏洞
**注意**: 需要网络连接，可能较慢

#### 10. **提交消息规范检查**
```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.6.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
```
**价值**: 强制规范的提交消息格式（如 `feat:`, `fix:`, `docs:`）

---

## GitHub Actions 增强

### 🎯 推荐新增工作流

#### 1. **依赖更新检查** (Dependabot 替代)
创建 `.github/workflows/dependency-review.yml`:
```yaml
name: Dependency Review
on: [pull_request]

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
```

**价值**: 在PR中检测新依赖的安全漏洞

#### 2. **代码覆盖率报告**
已有`pytest-cov`，可增强：

在 `.github/workflows/test.yml` 中添加：
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: false
```

**价值**: 可视化代码覆盖率趋势，在PR中显示覆盖率变化

#### 3. **CodeQL 安全分析**
创建 `.github/workflows/codeql.yml`:
```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # 每周日运行

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

**价值**: GitHub的高级安全扫描，发现深层次的安全问题

#### 4. **Benchmark 性能测试** (可选)
```yaml
name: Performance Benchmark

on:
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install pytest-benchmark
      - name: Run benchmarks
        run: pytest tests/benchmark/ --benchmark-only
```

---

## 本地开发工具

### 推荐的开发工具链

#### 1. **uvx 快速工具运行**
```bash
# 不安装直接运行工具
uvx ruff check .
uvx mypy guiguigui
uvx bandit -r guiguigui
```

#### 2. **make/justfile 简化命令**
创建 `Makefile`:
```makefile
.PHONY: test lint format check-all

test:
	uv run pytest

test-cov:
	uv run pytest --cov=guiguigui --cov-report=html --cov-report=term

lint:
	uv run ruff check guiguigui tests

format:
	uv run ruff format guiguigui tests

type-check:
	uv run mypy guiguigui

security:
	uv run bandit -r guiguigui -c pyproject.toml

check-all: lint type-check security test
	@echo "All checks passed!"

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache __pycache__
	rm -rf htmlcov .coverage coverage.xml
	rm -rf dist build *.egg-info

install-hooks:
	uv run pre-commit install --install-hooks
```

使用：
```bash
make test          # 运行测试
make check-all     # 运行所有检查
make install-hooks # 安装pre-commit hooks
```

#### 3. **VS Code 集成**
创建 `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "none",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.format.args": ["--config", "pyproject.toml"],
  "ruff.lint.args": ["--config", "pyproject.toml"]
}
```

---

## 持续集成最佳实践

### 🎯 当前CI状态
- ✅ 多Python版本测试 (3.10, 3.11, 3.12)
- ✅ 多平台测试 (Ubuntu, macOS, Windows)
- ✅ 代码质量检查 (ruff, mypy)
- ✅ 测试覆盖率报告

### 🔧 建议改进

#### 1. **矩阵测试优化**
```yaml
strategy:
  matrix:
    python-version: ['3.10']  # 当前只测3.10，可以在稳定后扩展
    os: [ubuntu-latest]        # 优先Linux，macOS在本地测
  fail-fast: false              # 不要快速失败，看到所有错误
```

#### 2. **缓存优化**
```yaml
- name: Cache uv
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}
    restore-keys: |
      ${{ runner.os }}-uv-
```

#### 3. **并行化测试**
```yaml
- name: Run tests in parallel
  run: uv run pytest -n auto  # 需要pytest-xdist
```

#### 4. **测试隔离**
```yaml
jobs:
  unit-tests:
    # 快速的单元测试
  integration-tests:
    # 较慢的集成测试
    needs: unit-tests
  platform-tests:
    # 平台特定测试
    needs: unit-tests
```

---

## 🚀 实施建议

### 阶段1: 立即实施（高ROI，低成本）
1. ✅ 添加 `no-commit-to-branch`
2. ✅ 添加 `debug-statements`
3. ✅ 添加 `check-ast`
4. ✅ 添加 `detect-private-key`
5. ✅ 添加 `bandit` 安全扫描

**预计时间**: 30分钟
**价值**: 防止90%的常见问题

### 阶段2: 渐进实施（提高代码质量）
6. ⏳ 启用Ruff的文档字符串检查（D系列规则）
7. ⏳ 添加 `codespell` 拼写检查
8. ⏳ 添加 CodeQL 到 GitHub Actions

**预计时间**: 1-2小时
**价值**: 提高代码可维护性

### 阶段3: 可选增强（针对特定需求）
9. 📌 依赖安全扫描
10. 📌 提交消息规范
11. 📌 性能基准测试
12. 📌 代码覆盖率趋势

---

## 📊 工具对比

| 工具 | 检查内容 | 速度 | 误报率 | 推荐度 |
|-----|---------|------|--------|--------|
| **ruff** | 代码风格+文档 | ⚡⚡⚡ 极快 | 低 | ⭐⭐⭐⭐⭐ 必须 |
| **mypy** | 类型检查 | ⚡⚡ 快 | 低 | ⭐⭐⭐⭐⭐ 必须 |
| **bandit** | 安全漏洞 | ⚡⚡ 快 | 中 | ⭐⭐⭐⭐⭐ 强烈推荐 |
| **codespell** | 拼写错误 | ⚡⚡⚡ 极快 | 中 | ⭐⭐⭐ 推荐 |
| **safety** | 依赖漏洞 | ⚡ 慢（网络） | 低 | ⭐⭐⭐ 可选 |
| **pylint** | 代码质量 | ⚡ 很慢 | 高 | ⭐⭐ 不推荐（ruff够用） |
| **pydocstyle** | 文档字符串 | - | - | ⭐ 已弃用（用ruff） |

---

## 🔍 常见问题

### Q: Pre-commit hooks会让提交变慢吗？
A: 会有一点，但通常<5秒。可以用：
- `git commit --no-verify` 跳过hooks（紧急时）
- `pre-commit run --files <file>` 只检查特定文件

### Q: 如何更新pre-commit hooks版本？
```bash
pre-commit autoupdate
```

### Q: Bandit报告了误报怎么办？
添加 `# nosec` 注释：
```python
password = get_password()  # nosec B105
```

### Q: 如何在CI中只运行变更的文件？
Pre-commit默认只检查变更文件，但在CI中：
```bash
pre-commit run --from-ref origin/main --to-ref HEAD
```

---

## 📚 参考资源

- [Pre-commit官方文档](https://pre-commit.com/)
- [Ruff规则列表](https://docs.astral.sh/ruff/rules/)
- [Bandit文档](https://bandit.readthedocs.io/)
- [Google Python风格指南](https://google.github.io/styleguide/pyguide.html)
- [GitHub Actions最佳实践](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
