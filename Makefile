.PHONY: check lint test typecheck fix db-up db-down db-logs

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

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-logs:
	docker compose logs -f postgres
