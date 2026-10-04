# Rules.md: Working Rules for the AI Assistant

**Project:** IT Help Desk and Asset Tracker (October-November 2026)
**Applies to:** Every session, every prompt, every file you touch in this project.

If any instruction in a prompt conflicts with a rule here, stop and ask me which one wins.

---

## 1. Working agreement

1. **Wait for my go-ahead.** Do not start building, editing files, or assigning me tasks until I explicitly say I'm ready. Finishing a deliverable is not permission to start the next one.
2. **One phase at a time.** Work only on the week or task I name. Do not pull work forward from later weeks.
3. **Ask before assuming.** If a requirement is ambiguous, ask one focused question. If I'm not available, state your assumption in writing and mark it `ASSUMPTION`.
4. **Plan, then build.** For any task that touches more than two files, show a short plan (files to create or change, in order) and wait for my approval before writing code.
5. **Small steps.** Prefer small, reviewable changes that I can run and verify. No large unreviewable dumps.
6. **Be honest.** If you are unsure, say so. If something I asked for is a bad idea, say so and explain why, then follow my decision.

## 2. Scope and stack lock

- **Fixed stack:** React (JavaScript, no TypeScript), FastAPI (Python), SQLAlchemy with Alembic, Pydantic, PostgreSQL, Clerk, Docker Compose, GitHub. Do not swap or add major technologies without asking.
- **Supporting tools:** Sentry (error tracking), BrowserStack (cross-browser testing), Azure or Heroku (deployment).
- **Roles:** `employee`, `staff`, `admin`. Do not invent new roles.
- **Out of scope unless I ask:** email notifications, file attachments, real-time updates, multi-tenancy, a mobile app, and anything in the Week 8 SLA enhancement before Week 8.
- Do not add libraries for convenience. Each new dependency needs a one-line justification and my approval.

## 3. Architecture rules (modular monolith)

- Four modules only: **Ticket, Asset, User, Report**. Each is its own Python package that owns its router, Pydantic schemas, service layer, and database models.
- Routers stay thin: declare the schema, call a service, return the response. Business logic lives in services.
- **A module never accesses another module's models directly.** Cross-module needs go through the other module's service.
- Shared code (config, database session, response helpers, exception handlers, auth dependencies) lives in one shared location, not copied into modules.
- The Report module is read-only. It never writes to another module's tables.
- Every architectural decision that is not obvious gets one line in the Decisions Log, including the alternative rejected.

## 4. API rules

- All routes live under `/api/v1/`. Use plural nouns and standard HTTP verbs.
- Every response uses the shared envelope. Errors use one consistent format with a machine-readable code and a human-readable message.
- List endpoints support pagination, filtering, and sorting. Set a maximum page size.
- Use correct status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 500). Never return 200 for an error.
- Every endpoint declares a Pydantic request schema and a `response_model`. Never return ORM objects or raw database rows directly.
- Every endpoint declares its allowed roles. No endpoint is public unless I say so (the health check is the only default exception).
- Ticket status changes follow the state machine in Architecture.md (Section 8). Reject invalid transitions with 409 or 422.

## 5. Database rules

- All schema changes go through Alembic migrations. Never edit the database by hand and never edit a migration that has already been merged; add a new one.
- Every migration has a working `downgrade()`.
- Use foreign keys, `NOT NULL` where appropriate, and CHECK constraints or enums for statuses.
- Index foreign keys and any column used in filters or sorting.
- Use SQLAlchemy or bound parameters. **Never build SQL with f-strings or string concatenation from user input.**
- Seeders contain fake data only. Never commit real names, emails, or serial numbers.
- Keep ticket status history append-only.

## 6. Authentication and security rules

- Clerk owns credentials. **Never store, log, or transmit passwords locally.**
- The API verifies every Clerk token: signature, expiry, not-before, issuer, and authorized party. A request with a missing or invalid token gets 401.
- **Never trust the client for roles or ownership.** Resolve the role server-side and check ownership in the service layer (an employee sees only their own tickets).
- Authorization is checked on every endpoint, not just in the UI. Hiding a button is not security.
- Validate all input on the server, even if the frontend validates too. Use separate Pydantic schemas for create, update, and response, so clients cannot set fields such as role, status, or ownership unless allowed. Never mass-assign request bodies into models.
- No secrets in the repository, ever. Use `.env` files that are gitignored, plus a committed `.env.example` with placeholder values. If a secret is committed by mistake, tell me immediately so I can rotate it.
- Configure `CORSMiddleware` with known origins only. Production runs with debug off, and `/docs` and `/redoc` are disabled or protected unless I decide otherwise.
- Do not log tokens, full request bodies, or personal data. Scrub them before sending anything to Sentry.
- Run `pip-audit` and `npm audit` before any release and report the results.

## 7. Frontend rules

- Feature-based folders. Components stay small and single-purpose.
- Server data goes through one API client that attaches the Clerk token. No component calls `fetch` directly.
- Protected routes and role-based UI are for usability only; the API is the real gate.
- Every form shows loading, success, and error states, with specific error messages.
- Mobile-first layout. Accessible by default: labels on inputs, keyboard navigation, sufficient contrast.
- No secrets in frontend code. Only the Clerk publishable key belongs there.

## 8. Code quality and testing

- Follow PEP 8 enforced by ruff, with type hints on every function, and the project ESLint/Prettier config for JavaScript. Do not mix blocking and async code; follow the sync or async choice recorded in the Decisions Log. Names are descriptive; comments explain *why*, not *what*.
- No dead code, commented-out blocks, or leftover debug output.
- Every service method and endpoint gets pytest tests: at least one happy path, one validation failure, and one authorization failure.
- A task is not done until the tests pass and you have told me how to run them.
- Report bugs you notice outside the current task. Do not fix them silently.

## 9. Git and GitHub rules

- Branches: `main` (stable) and `feature/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
- Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`), one logical change each.
- Suggest a commit message with every completed task. Do not push, merge, or force-push on my behalf.
- CI (lint, tests, dependency audit) must pass before merging to `main`.

## 10. Docker and environment rules

- `docker compose up` must bring up the full stack from a clean clone, with documented setup steps.
- Pin image versions and the Python version. Do not use `latest`. Pin Python dependencies with a lock file or exact versions.
- Keep development and production configuration separate and clearly labeled.
- Database data lives in a named volume. Document how to reset it.

## 11. Documentation rules

- Update the README whenever setup, commands, or environment variables change.
- **Bullet limits for readability:** in any documentation you write (README, manual, workflow notes, testing record notes), every bullet list must have a minimum of 2 and a maximum of 5 bullets. If a list needs more than 5 items, group the items under subheadings or split it into separate lists. Never write a single-bullet list; write a sentence instead.
- Keep the Decisions Log current.
- Manual guides follow one template: **purpose, required role, prerequisites, numbered steps, expected result**.
- The workflow diagram is Mermaid, kept in the repo, and updated whenever the ticket flow changes.
- Every workflow gets a testing record entry: workflow, steps, expected result, actual result, browser/device, date.
- Screenshots are real captures from the running app using seeded fake data, saved in a consistent folder with descriptive filenames.

## 12. Communication rules

- Lead with the answer, then the reasoning. Keep it short.
- When you hand back work, use this order: **what changed, how to run or verify it, what to check, what is next (only after I ask)**.
- Use tables for comparisons and endpoint lists, and code blocks for commands and code.
- Explain trade-offs in plain language. I need to be able to defend every decision in this project.
- Flag friction with my fixed decisions as soon as you see it, with a recommended workaround.

## 13. Definition of done (for every task)

- [ ] Works locally via `docker compose up`
- [ ] Input validated and authorization enforced server-side
- [ ] Tests written and passing
- [ ] No secrets, debug output, or dead code committed
- [ ] README and Decisions Log updated if affected
- [ ] Suggested commit message provided
- [ ] I have confirmed it meets the exit criteria for the current week
