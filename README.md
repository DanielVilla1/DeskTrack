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
.github/workflows/    CI
Weekly-Prompt-Plan.md Week-by-week build plan
```

## Getting started

Setup steps will be filled in as the project is built.

```
# Planned
docker compose up --build
```

Configuration (Clerk keys, database URL) will be provided through environment variables. Never commit secrets.

## Documentation

- [Architecture](system-architecture/Architecture.md)
- [Rules](system-architecture/Rules.md)
- [Weekly Prompt Plan](Weekly-Prompt-Plan.md)
- User manual, workflow, and testing notes: `docs/`

## Status

Early stage: project structure is in place and implementation is in progress.
