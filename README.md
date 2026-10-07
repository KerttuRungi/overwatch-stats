# Overwatch Stats

Overwatch Stats is a full-stack project for collecting and comparing Overwatch player profile data. The app fetches player information from the public [OverFast API](https://overfast-api.tekrop.fr), stores selected players in a local database, and presents a comparison list in the frontend.

## Why this project exists

The goal is to practice building a complete data flow:
- fetch player data from an external public API,
- validate and transform it into app-specific models,
- persist comparison targets,
- and serve that data to a frontend UI.

## Project functionality

- Search a player by BattleTag format (`username-1234`)
- Fetch player profile data from OverFast through the backend
- Add players to a comparison list stored in the database
- Remove players from the comparison list
- List all stored players for comparison
- Fetch player stats summary endpoint via backend proxy

## Tech stack

- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + SQLModel + Alembic
- **Database driver:** Psycopg (configure your own PostgreSQL `DATABASE_URL`)
- **Dependency managers:** `npm` (frontend), `uv` (backend)

## Repository structure

- `/home/runner/work/overwatch-stats/overwatch-stats/overwatch-stats/frontend`
- `/home/runner/work/overwatch-stats/overwatch-stats/overwatch-stats/overwatch-backend`

## Local setup

### 1) Backend setup

From:
`/home/runner/work/overwatch-stats/overwatch-stats/overwatch-stats/overwatch-backend`

Create a `.env` file with:

```env
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:5432/<database>
```

Install dependencies:

```bash
uv sync --locked --group dev
```

Run backend server:

```bash
uv run fastapi dev src/main.py --port 8000
```

### 2) Frontend setup

From:
`/home/runner/work/overwatch-stats/overwatch-stats/overwatch-stats/frontend`

Create a `.env` file with:

```env
VITE_API_URL=http://localhost:8000
```

Install dependencies:

```bash
npm ci
```

Run frontend:

```bash
npm run dev
```

## Database migrations

From:
`/home/runner/work/overwatch-stats/overwatch-stats/overwatch-stats/overwatch-backend`

Apply migrations:

```bash
uv run alembic upgrade head
```

Create a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe_change"
```

> Note: Alembic uses `DATABASE_URL` from your backend `.env`.

## CI pipeline

GitHub Actions workflow (`.github/workflows/python-app.yml`) runs on push and pull requests.

It has two jobs:
- **backend:** installs dependencies with `uv`, then runs `pytest`
- **frontend:** installs dependencies with `npm ci`, then runs `npm run build`

The backend endpoints tested in CI use mocked OverFast responses in unit tests, while runtime application behavior depends on the public OverFast API availability.
