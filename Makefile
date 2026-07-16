.PHONY: check lint test typecheck fix

check: lint typecheck test

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

test:
	uv run pytest

fix:
	uv run ruff check . --fix
	uv run ruff format .