# AI Job Search Operations Assistant

## Problem

Reviewing vacancies, choosing a resume, and deciding whether to apply are currently manual steps. This service turns vacancy text into a structured recommendation.

## Current scope

The first vertical slice exposes `POST /api/v1/vacancies/analyze`. It accepts:

```json
{"vacancy_text": "Python FastAPI developer"}
```

and returns an `apply`, `apply_with_caveats`, or `skip` decision with matched requirements and reasoning. The current analyzer is deterministic and checks for `python` and `fastapi`; it is deliberately not an LLM integration.

## Run locally

```bash
uv sync
uv run fastapi dev main.py
```

Open Swagger UI at `http://127.0.0.1:8000/docs`. Run verification with:

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

## Next slice and carry-over

The next slice is an LLM-backed analyzer behind the existing `VacancyAnalyzer` contract. The API, deterministic decision branches, analyzer unit tests, and endpoint tests are ready. External integrations, persistence, queues, authentication, and a real-vacancy manual check remain out of scope for this slice.
