# DeskTrack: IT Help Desk and Asset Tracker

A web system for a small organization to manage technical support requests and keep track of its computers and network equipment.

## Project goal

Build and deploy a secure, documented portfolio project that demonstrates full-stack development, database design, networking, and IT support skills.

## Users and roles

| Role | What they can do |
|------|------------------|
| **Employee** | Submit support tickets and track their status |
| **IT staff** | Assign tickets, update their status, and resolve them |
| **Admin** | Manage user access and create or update equipment records |

## Main workflow

1. An employee submits a ticket.
2. IT staff assign the ticket and update its status.
3. The issue is resolved.

Admins can also add or update equipment (computers and network devices) at any time.

## Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | React (JavaScript) with Vite |
| Backend API | FastAPI (Python 3.12), SQLAlchemy 2.x, Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Authentication | Clerk (sign-in in React; the API verifies Clerk session tokens) |
| Local infrastructure | Docker Compose |

> The original overview mentioned PHP with CodeIgniter. The architecture document chose FastAPI instead, so this README follows it.

## Repository layout

```
backend/              FastAPI app (core, users, tickets, assets, reports), Alembic migrations, tests
frontend/             React app (features: tickets, assets, users, reports)
docs/                 User manual, workflow, screenshots, testing notes
system-architecture/  Architecture.md and Rules.md
.github/workflows/    CI (Dependabot config sits one level up)
docker-compose.yml    Local stack: database, API, web
Weekly-Prompt-Plan.md Week-by-week build plan
```

## Backend modules

The API is a modular monolith. Modules call each other's services, never each other's models.

| Module | Owns | Does not own |
|--------|------|--------------|
| `users` | Local user records, roles, lazy creation on first login, `GET /me` | Credentials (Clerk) |
| `tickets` | Tickets, comments, status history, assignment, the status state machine | Asset and user records |
| `assets` | Assets, categories, assignments to users, the asset lifecycle | Tickets |
| `reports` | Read-only aggregate queries for dashboards | Any writes |

## Getting started

### Prerequisites

- Docker Desktop with Compose v2
- Git
- A free [Clerk](https://clerk.com) account with one development application
- Python 3.12 or newer and Node.js 24 LTS on your machine, only for the pre-commit hooks

### Setup from a clean clone

1. Clone the repository and open it.

   ```bash
   git clone https://github.com/DanielVilla1/DeskTrack.git
   cd DeskTrack
   ```

2. Copy the three example environment files. On PowerShell, use `Copy-Item` instead of `cp`.

   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Edit the copies.

   | File | Change |
   |------|--------|
   | `.env` | Set `POSTGRES_PASSWORD` |
   | `backend/.env` | Use the same password inside `DATABASE_URL` |
   | `frontend/.env` | Set `VITE_CLERK_PUBLISHABLE_KEY` from the Clerk dashboard under API keys |

4. Start the stack.

   ```bash
   docker compose up --build
   ```

5. Open the app.

   | Address | What you see |
   |---------|--------------|
   | http://localhost:5173 | React app (redirects to the Clerk sign-in page) |
   | http://localhost:8000/api/v1/health | `{"data":{"status":"ok"}}` |
   | http://localhost:8000/docs | Interactive API docs (development only) |

### Environment variables

| Variable | File | Purpose |
|----------|------|---------|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | `.env` | Creates the database container |
| `DATABASE_URL` | `backend/.env` | Connection string used by the API and Alembic |
| `ENVIRONMENT` | `backend/.env` | `development` or `production`; production turns off `/docs` and `/redoc` |
| `CORS_ORIGINS` | `backend/.env` | Comma-separated frontend origins the API accepts |
| `VITE_CLERK_PUBLISHABLE_KEY`, `VITE_API_BASE_URL` | `frontend/.env` | Clerk key and API address for the React app |

The Clerk variables for the API arrive when token verification is built. Never commit a `.env` file.

### Everyday commands

Run these from the repository root while the stack is up.

| Task | Command |
|------|---------|
| Backend tests | `docker compose exec api pytest` |
| Backend lint and format check | `docker compose exec api ruff check .` and `docker compose exec api ruff format --check .` |
| Frontend checks | `docker compose exec web npm run lint`, `format:check`, `test`, and `build` |
| Apply database migrations | `docker compose exec api alembic upgrade head` |
| Stop the stack | `docker compose down` |
| Reset the database (deletes all data) | `docker compose down -v` |

After you change `package.json` or `requirements.txt`, rebuild with `docker compose up --build -V`.

The database, API, and web ports are bound to `127.0.0.1`, so only your own machine can reach them.

### Updating pinned Python dependencies

Both requirements files pin every package, including transitive ones, using `pip freeze` inside the same Python image Docker and CI use. To refresh them:

1. Print the new runtime pins and replace the package lines in `backend/requirements.txt`, keeping its header and the `uvloop` marker `; sys_platform != "win32"`.

   ```bash
   docker run --rm python:3.12.15-slim sh -c 'pip install -q fastapi "uvicorn[standard]" sqlalchemy "psycopg[binary]" alembic pydantic-settings && pip freeze'
   ```

2. Print the development pins, then copy only the lines that are not already in `requirements.txt` into `backend/requirements-dev.txt`.

   ```bash
   docker run --rm -v "$PWD/backend:/src:ro" python:3.12.15-slim sh -c 'pip install -q -r /src/requirements.txt pytest httpx ruff pre-commit pip-audit && pip freeze'
   ```

3. Rebuild with `docker compose up --build -V`, then run the backend tests and `docker compose exec api pip-audit --no-deps -r requirements.txt`.

### Known limitations

A 500 response from an unhandled error has no CORS headers, because Starlette's error middleware sits outside the CORS middleware. A browser reports it as a CORS failure, so check the API logs or `/docs` to see the real status.

### Code quality hooks

Install the hooks once so ruff, Prettier, and ESLint run before every commit. CI runs the same checks.

```bash
pip install pre-commit
npm --prefix frontend ci
pre-commit install
```

## Documentation

- [Architecture](system-architecture/Architecture.md)
- [Rules](system-architecture/Rules.md)
- [Weekly Prompt Plan](Weekly-Prompt-Plan.md)
- User manual, workflow, and testing notes: `docs/`

## Status

Early stage: the Week 1 scaffold is in place (Docker Compose stack, API health endpoint, React shell with Clerk, CI, and pre-commit hooks). Ticket features start in Week 2.
