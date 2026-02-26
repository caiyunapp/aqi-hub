.PHONY: help build fmt lint sync lock upgrade all test docs-serve docs-serve-versioned

export UV_PYTHON_PREFERENCE=only-system
export PYTHONPATH := $(shell pwd)
export PYTHON := python3

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build       Build the project"
	@echo "  fmt         Format the code"
	@echo "  lint        Lint the code"
	@echo "  sync        Sync the dependencies"
	@echo "  lock        Lock the dependencies"
	@echo "  upgrade     Upgrade the dependencies"
	@echo "  all         Build, format, lint, sync, lock, and upgrade"
	@echo "  test        Run the tests"
	@echo "  docs-serve  Run MkDocs dev server (single-version preview)"
	@echo "  docs-serve-versioned  Run mike serve (multi-version preview with version selector)"
	
build:
	uv build --no-sources

fmt:
	uv run ruff check --select I --fix .
	uv run ruff format .

lint:
	uv run ruff check .
	uv run ruff format --check .

fix:
	uv run ruff check --fix .
	uv run ruff format .

sync:
	uv sync --compile

lock:
	uv lock

upgrade:
	uv lock --upgrade

all: lock sync
	make fmt
	make lint
	git diff --exit-code || (echo "Please run 'make fmt' and 'make lint' or commit changes to fix the above issues." && exit 1)

test: lint
	uv run pytest -v .

docs-serve:
	uv run mkdocs serve

# 多版本文档本地预览（与 GitHub Pages 一致的版本选择器）
# 首次运行会先 deploy 一次 latest 并设为默认，再启动 mike serve。
# 根路径 / 会跳转到默认版本；页面顶部有版本下拉框可切换。
# 若要在本地看到多个版本（如 0.3.0、0.2.1），需先分别 deploy 再 serve，例如：
#   git checkout v0.2.1 && uv run mike deploy 0.2.1 && git checkout main
#   uv run mike deploy latest && uv run mike deploy 0.3.0
#   uv run mike set-default latest && uv run mike serve
docs-serve-versioned:
	uv run mike deploy latest
	uv run mike set-default latest
	uv run mike serve
