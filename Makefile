BACKEND_DIR := backend

.PHONY: check lint test typecheck fix \
	backend-check backend-lint backend-test backend-typecheck backend-fix backend-dev \
	db-up db-down db-logs

check: backend-check

lint: backend-lint

typecheck: backend-typecheck

test: backend-test

fix: backend-fix

backend-check: backend-lint backend-typecheck backend-test

backend-lint:
	cd $(BACKEND_DIR) && uv run ruff check .

backend-typecheck:
	cd $(BACKEND_DIR) && uv run mypy .

backend-test:
	cd $(BACKEND_DIR) && uv run pytest

backend-fix:
	cd $(BACKEND_DIR) && uv run ruff check . --fix
	cd $(BACKEND_DIR) && uv run ruff format .

backend-dev:
	cd $(BACKEND_DIR) && uv run fastapi dev main.py

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-logs:
	docker compose logs -f postgres