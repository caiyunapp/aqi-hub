export UV_PYTHON_PREFERENCE=only-system
export PYTHONPATH := $(shell pwd)

fmt:
	uv run ruff check --select I --fix .
	uv run ruff format .

lint:
	uv run ruff check .
	uv run ruff format --check .

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
