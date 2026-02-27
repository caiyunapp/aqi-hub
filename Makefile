.PHONY: help build develop fmt lint sync lock upgrade all test docs docs-rust

export UV_PYTHON_PREFERENCE=only-system
export PYTHONPATH := $(shell pwd)
export PYTHON := python3

CRATE := aqi-hub
RUFF := uv run ruff

help:
	@echo "Usage: make [target]"
	@echo "  build    Python wheel"
	@echo "  develop  Install native extension (maturin)"
	@echo "  fmt      Format code (ruff + cargo fmt)"
	@echo "  lint     Check style & clippy"
	@echo "  sync     uv sync --compile"
	@echo "  lock     uv lock"
	@echo "  upgrade  uv lock --upgrade"
	@echo "  all      lock, sync, fmt, lint, diff"
	@echo "  test     Lint + pytest + cargo test"
	@echo "  docs     MkDocs serve"
	@echo "  docs-rust  cargo doc --open"

build:
	uv build --no-sources

develop:
	uv run maturin develop --release

fmt:
	$(RUFF) check --fix .
	$(RUFF) format .
	cargo fmt

lint:
	$(RUFF) check .
	$(RUFF) format --check .
	cargo fmt -- --check
	cargo clippy -p $(CRATE)

sync:
	uv sync --compile

lock:
	uv lock

upgrade:
	uv lock --upgrade

all: lock sync
	$(MAKE) fmt
	$(MAKE) lint
	@git diff --exit-code || (echo "Run 'make fmt' and 'make lint' or commit." && exit 1)

test: lint
	uv run pytest -v .
	cargo test -p $(CRATE)

docs:
	uv run mkdocs serve

docs-rust:
	cargo doc -p $(CRATE) --no-deps --open
