# AI Job Search Operations Assistant

An authenticated workspace for turning vacancy descriptions into structured,
candidate-specific application decisions.

The application stores the user's target roles, relevant keywords, accepted
work modes, and optional resume labels. It sends those preferences together
with a vacancy title and description to OpenAI and returns an `apply`,
`apply_with_caveats`, or `skip` decision with supporting evidence.

## Current capabilities

The backend currently supports:

- account registration and JWT bearer authentication;
- retrieval of the authenticated user;
- per-user job-preference storage;
- replace-all editing of target roles, keywords, work modes, and resume labels;
- OpenAI structured vacancy analysis against the authenticated user's saved
  preferences;
- validation that positive recommendations reference an existing preference
  and its configured resume;
- PostgreSQL persistence managed through SQLAlchemy and Alembic.

The React workspace currently includes routing, authentication state,
protected routes, a shared HTTP client, and Mantine 9. The user-facing forms
and job-search screens are being completed incrementally.

## Architecture

The repository contains two applications:

```text
.
├── backend/                  # FastAPI, application/domain code, persistence
│   ├── app/
│   │   ├── auth/
│   │   ├── job_preferences/
│   │   ├── vacancies/
│   │   └── infrastructure/
│   ├── migrations/          # Alembic migrations
│   ├── tests/
│   └── main.py
├── frontend/                 # React, TypeScript, Vite, Mantine
│   └── src/
│       ├── app/
│       ├── features/
│       └── shared/
├── docker-compose.yaml       # local PostgreSQL
└── Makefile                  # workspace development commands
```

Backend modules are organized by business capability. FastAPI routes remain
thin, while authentication, preference replacement, analysis orchestration,
and persistence live behind their corresponding boundaries. The React
application acts as a delivery adapter and does not duplicate backend matching
or authorization rules.

## Requirements

- Python 3.12;
- [uv](https://docs.astral.sh/uv/);
- Node.js and npm;
- Docker with Docker Compose;
- an OpenAI API key for real vacancy analysis.

## Environment

Create the local environment file:

```bash
cp .env.example .env
```

Set these values in the root `.env`:

```dotenv
OPENAI_API_KEY=
POSTGRES_PASSWORD=
DATABASE_URL=postgresql+psycopg://job_search:<POSTGRES_PASSWORD>@localhost:5432/job_search
JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

`POSTGRES_PASSWORD` and the password inside `DATABASE_URL` must match. Use a
long random value for `JWT_SECRET_KEY`. Never commit `.env`.

## Run locally

Start PostgreSQL from the repository root:

```bash
make db-up
```

Install backend dependencies and apply migrations:

```bash
cd backend
uv sync
uv run alembic upgrade head
cd ..
```

Start FastAPI:

```bash
make backend-dev
```

In another terminal, install and start the React application:

```bash
cd frontend
npm install
npm run dev
```

Local services:

- React UI: `http://localhost:5173`;
- Swagger UI: `http://127.0.0.1:8000/docs`;
- health check: `http://127.0.0.1:8000/health`.

Vite proxies relative `/api` requests to the FastAPI development server.

## API overview

All feature endpoints use the `/api/v1` prefix.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/auth/register` | Register a user |
| `POST` | `/auth/token` | Exchange form-encoded credentials for a bearer token |
| `GET` | `/auth/me` | Retrieve the authenticated user |
| `GET` | `/job-preferences` | List the authenticated user's preferences |
| `PUT` | `/job-preferences` | Replace the authenticated user's preferences |
| `POST` | `/vacancies/analyze` | Analyze a vacancy against saved preferences |

Job-preference and vacancy-analysis endpoints require an
`Authorization: Bearer <token>` header. Vacancy analysis requires at least one
saved job preference.

## Verification

Run backend and frontend checks from the repository root:

```bash
make check
```

Run frontend checks:

```bash
cd frontend
npm run lint
npm run format:check
npm run build
```

Useful database commands:

```bash
make db-logs
make db-down
```

## Project documentation

- [Frontend development](frontend/README.md)
