.PHONY: help build fmt lint sync lock upgrade all test docs-serve

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
	@echo "  docs-serve  Run MkDocs dev server (uv run mkdocs serve)"
	
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
