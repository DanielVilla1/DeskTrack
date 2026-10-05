# Week 1: review and follow-up

The Week 1 scaffold was reviewed against `Rules.md` and the Week 1 row of `Architecture.md` section 18. This file records what was fixed, what waits for a later week, and what is accepted as is.

## Fixed in Week 1

- All Python dependencies are pinned, including transitive ones.
- Unknown routes, wrong methods, validation errors, and unhandled errors use the shared error envelope.
- The API and web ports are bound to `127.0.0.1`.
- `database_url` is a `SecretStr`, so the password stays out of `repr()` and logs.
- Decisions Log entries are drafted in `decisions-log-entries.md`.

## Deferred, grouped by week

### Week 2

- Add a database connectivity test.
- Write tests for each new feature as it is built.
- Clerk variables become required in `Settings`, so update the existing `.env` files at that point.

### Week 5

- Reject a wildcard in `CORS_ORIGINS`.
- Pin GitHub Actions to commit SHAs.
- Add the Dependabot `docker` ecosystem so the pinned image tags are updated.
- Re-check ESLint 10 support in `eslint-plugin-react`, and add a Dependabot ignore for the ESLint major until it works.

### Week 6

- Remove duplication: the repeated health URL in tests, `compare_type=True` in `env.py`, and the Postgres image tag in two files.
- Replace the three docs-URL conditionals in `main.py` with one mapping.
- Strengthen the weak `toBeTruthy()` assertions in the frontend tests.
- Reword the `HomePage` placeholder text.

### Week 7

Containers run as root in development. The production images should run as a non-root user.

## Accepted as is

- The engine, session factory, and `get_db` are unused until Week 2.
- The health endpoint has only happy-path and wrong-method tests, because it takes no input and is public.
- The `alembic/` folder keeps its name, although it shares a name with the library.
- Committing without `frontend/node_modules` gives a cryptic pre-commit error, which the README already documents.

## Week 2 prep proposals

Nothing below is implemented. Each one waits for approval at the start of Week 2.

### Clerk package

Move from `@clerk/clerk-react` to `@clerk/react`. Eight files change, and in seven of them only the import string changes: `package.json`, five source files, and two test files. Check `ClerkProvider` and the sign-in props against the installed types before the move.

### Test database

Add a `db-test` Compose service with its data on `tmpfs`, and read `TEST_DATABASE_URL` only in `conftest.py`. The tests refuse a database whose name does not end in `_test`. Run `alembic upgrade head` once per session, and roll back a transaction after each test.

### Alembic model registration

Import each module's models in `alembic/env.py`, one line per module with a `noqa: F401` comment. Add `known-third-party = ["alembic"]` to the ruff isort settings so `alembic` is not sorted as first-party.

## Known limitation

A 500 response from an unhandled error has no CORS headers, because Starlette's error middleware sits outside the CORS middleware. A browser reports it as a CORS failure, so check the API logs to see the real status.
