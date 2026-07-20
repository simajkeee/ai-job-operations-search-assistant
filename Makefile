BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: check lint test typecheck fix \
	backend-check backend-lint backend-test backend-typecheck backend-fix backend-dev \
	frontend-check frontend-lint frontend-format-check frontend-build frontend-dev \
	db-up db-down db-logs

check: backend-check frontend-check

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

frontend-check: frontend-lint frontend-format-check frontend-build

frontend-lint:
	cd $(FRONTEND_DIR) && npm run lint

frontend-format-check:
	cd $(FRONTEND_DIR) && npm run format:check

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

frontend-dev:
	cd $(FRONTEND_DIR) && npm run dev

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-logs:
	docker compose logs -f postgres
