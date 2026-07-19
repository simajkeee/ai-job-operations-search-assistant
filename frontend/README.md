# AI Job Search Operations Assistant — frontend

React application for managing job preferences and analyzing vacancies against
the authenticated user's profile.

## Stack

- React 19;
- TypeScript;
- Vite;
- React Router;
- Mantine 9;
- browser `fetch` through the shared HTTP client;
- ESLint and Prettier.

Mantine provides standard UI primitives. The initial dependency scope is
`@mantine/core` and `@mantine/hooks`; additional Mantine packages are added only
for concrete feature needs. Application code remains organized by business
feature rather than by component-library type.

## Development

Run commands from `frontend/`:

```bash
npm install
npm run dev
npm run lint
npm run format:check
npm run build
```

During local development, Vite proxies relative `/api` requests to the FastAPI
backend at `http://127.0.0.1:8000`.

Start the backend separately from the repository root:

```bash
make backend-dev
```

## Source structure

- `src/app/` composes providers, routing, and the application layout;
- `src/features/` contains feature-specific UI, state, and API contracts;
- `src/shared/` contains the shared HTTP client and genuinely reusable UI
  concerns.
