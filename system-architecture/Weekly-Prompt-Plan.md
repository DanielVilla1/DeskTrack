# Weekly Prompt Plan: IT Help Desk and Asset Tracker

A prompt kit for each phase of your roadmap. Each week has a goal, exit criteria, and ready-to-paste prompts you can polish before use.

**Assumption:** Your roadmap starts at Week 2, so Week 1 is treated as setup (repo, Docker Compose, Clerk app). Adjust if your calendar differs.

---

## How to use this plan

1. Start every session with the **Session Starter** (below) and make sure `Architecture.md` and `Rules.md` are in the repo's `system-architecture/` folder (or attach them if your AI cannot read the folder).
2. Paste the week's prompt only when you are ready to build. The rules tell the AI to wait for you.
3. Review the result against the week's **exit criteria**.
4. Run the **Review and Polish** prompt, then the **Close-out** prompt before ending the session.

---

## Reusable prompts

### Session Starter

```
You are my senior full-stack engineer on the IT Help Desk and Asset Tracker project.

Read system-architecture/Architecture.md and system-architecture/Rules.md. Follow both strictly.

Current week: [WEEK NUMBER AND NAME]
Where I left off: [one or two sentences, or "starting fresh"]

Confirm in 3 bullets: (1) the stack, (2) the current week's scope, (3) anything unclear.
Then stop and wait until I say I'm ready.
```

### Review and Polish (run after each task)

```
Review what you just built against Rules.md and this week's exit criteria.

Report in this order:
1. Rule violations (with file and line)
2. Security or validation gaps
3. Missing or weak tests
4. Code cleanliness against Rules.md section 8 (function and file size, duplication, naming, magic values, unused code) and readability improvements
5. Anything that will cause problems in a later week

List findings by severity. Do not change any code yet. Wait for me to pick which to fix.
```

### Close-out (end of each session)

```
Wrap up this session.

1. Summarize what is done, what is partly done, and what is not started.
2. List open questions and assumptions I still need to confirm.
3. For each logical change, give me the suggested branch name, the files to include, and a Conventional Commits message, in the order I should commit them. I make all branches and commits myself, so do not run any git command that changes the repository.
4. Update the Decisions Log with any new decisions.
5. Write a 5-line "Where I left off" note I can paste into the next Session Starter.
```

---

## Week 1: Setup

**Goal:** A clean repo where `docker compose up` starts the whole stack, with a verified Clerk connection.

**Exit criteria**
- [x] Repo created with the agreed structure, `.gitignore`, `.env.example`, README skeleton
- [x] Compose services running: React, FastAPI API (uvicorn), PostgreSQL
- [x] Alembic initialized and the first migration runs
- [x] OpenAPI docs reachable at `/docs` in development
- [x] `GET /api/v1/health` returns the standard envelope
- [x] Clerk application created and keys stored in `.env`
- [x] GitHub repo with branch protection and a basic CI workflow (lint and tests)
- [x] Pre-commit hooks installed; CI runs lint and format checks
- [x] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 1A: Plan the scaffold**
```
Week 1, Setup. Following Architecture.md, propose a scaffold plan:
the repo tree, the Docker Compose services (ports, volumes, network), the .env.example
contents, and the CI workflow outline. List files in the order you would create them.
Do not write code yet. Wait for my approval.
```

**Prompt 1B: Build the scaffold**
```
Plan approved. Build the Week 1 scaffold now: repo structure, Docker Compose,
FastAPI with the four empty module packages (Ticket, Asset, User, Report),
Alembic setup, shared response envelope, health endpoint, React app shell, ruff, ESLint, and Prettier configuration, pre-commit hooks, and the README setup section.
Give me the exact commands to run it and verify it from a clean clone.
```

---

## Week 2: Core functionality, part 1 (Auth, users, ticket submission and tracking)

**Goal:** A signed-in employee can submit a ticket and see its status.

**Exit criteria**
- [ ] Clerk sign-in works in React; protected routes in place
- [ ] API verifies Clerk tokens through an auth dependency; invalid tokens get 401
- [ ] Local user created on first authenticated request, with the default `employee` role
- [ ] Alembic migrations for `users`, `tickets`, `ticket_status_history`
- [ ] Employee can create a ticket and view only their own tickets and each ticket's status
- [ ] Tests: happy path, validation failure, authorization failure for each endpoint
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 2A: Authentication and user module**
```
Week 2, part A. Implement authentication and the User module per Architecture.md:
the Clerk token verification dependency, user creation on first login, role resolution,
the users migration, and a GET /api/v1/me endpoint.
Show a plan first, then wait for my approval. Include tests for missing, expired,
and tampered tokens.
```

**Prompt 2B: Ticket submission and tracking (API)**
```
Week 2, part B. Implement the Ticket module's employee features:
migrations for tickets and ticket_status_history, POST /api/v1/tickets,
GET /api/v1/tickets (own tickets only, with pagination and filtering by status),
and GET /api/v1/tickets/{id} (ownership enforced).
Initial status is "open" and the first history row is written on creation.
Plan first, wait for approval, then include tests.
```

**Prompt 2C: Ticket submission and tracking (React)**
```
Week 2, part C. Build the React pages for employees: a ticket submit form,
a "My Tickets" list with status badges, and a ticket detail page.
Use the shared API client that attaches the Clerk token. Every form needs
loading, success, and error states. Plan first, wait for approval.
```

---

## Week 3: Core functionality, part 2 (Staff workflow)

**Goal:** Staff can assign, update, and resolve tickets, with a full audit trail.

**Exit criteria**
- [ ] Staff queue lists all tickets with filtering by status and assignee
- [ ] Staff can assign a ticket, change its status along the allowed state machine, and resolve it
- [ ] Comments on tickets (employee and staff), with visibility rules
- [ ] Every status change recorded in `ticket_status_history` with actor and timestamp
- [ ] Employees cannot call staff endpoints (403 verified by tests)
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 3A: Staff ticket operations (API)**
```
Week 3, part A. Extend the Ticket module for staff: GET /api/v1/tickets with all-ticket
visibility for staff and admin, PATCH /api/v1/tickets/{id}/assign,
PATCH /api/v1/tickets/{id}/status (enforcing the state machine), and resolve behavior
(resolved_at set). Write a status_history row on every change.
Plan first, wait for approval, then include role-based authorization tests.
```

**Prompt 3B: Comments (API)**
```
Week 3, part B. Add ticket comments: migration for ticket_comments,
POST and GET /api/v1/tickets/{id}/comments. Employees can comment only on their own
tickets; staff can comment on any. Plan first, wait for approval, include tests.
```

**Prompt 3C: Staff UI**
```
Week 3, part C. Build the React staff experience: a ticket queue with filters,
a ticket detail view with assign, status change, resolve, and a comments thread
and status history timeline. Role-based UI should hide staff actions from employees,
though the API remains the real gate. Plan first, wait for approval.
```

---

## Week 4: Core functionality, part 3 (Assets and admin summaries)

**Goal:** Admins can manage equipment records and see ticket and asset summaries.

**Exit criteria**
- [ ] Migrations for `asset_categories`, `assets`, `asset_assignments`
- [ ] Admin can create, edit, and retire assets; assign an asset to a user
- [ ] Tickets can optionally link to an asset
- [ ] Report module returns tickets by status, assets by status, and warranty expiring soon
- [ ] Admin dashboard in React showing those summaries
- [ ] Non-admins get 403 on asset-write and report endpoints
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 4A: Asset module (API)**
```
Week 4, part A. Implement the Asset module: migrations for asset_categories, assets,
and asset_assignments (serial number unique, status, purchase date, warranty expiry,
location), CRUD endpoints, and assignment and return of an asset to a user.
Add the optional ticket-to-asset link through the Asset module's service,
not by reaching into its model from the Ticket module.
Plan first, wait for approval, include tests.
```

**Prompt 4B: Report module**
```
Week 4, part B. Implement the read-only Report module: tickets by status,
assets by status, and assets with warranty expiring within N days.
Use efficient SQL and explain whether views or queries are better here.
Admin-only endpoints. Plan first, wait for approval, include tests.
```

**Prompt 4C: Admin UI**
```
Week 4, part C. Build the React admin area: asset list with search and filters,
asset create and edit form, assignment flow, and a dashboard with the three summaries.
Plan first, wait for approval.
```

---

## Week 5: Security

**Goal:** A documented security review with the important findings fixed and verified.

**Exit criteria**
- [ ] Review report covering login, role permissions, input validation, password handling, database access, secrets, dependencies, and deployment settings
- [ ] Every endpoint verified for token check and role check, backed by a test
- [ ] No secrets in the repo or git history; `.env.example` complete
- [ ] `pip-audit` and `npm audit` clean or each finding triaged
- [ ] Production settings checklist completed (debug off, CORS locked, secure headers, `/docs` restricted)
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 5A: Security audit (findings only)**
```
Week 5, Security. Audit the whole project against Rules.md section 6 and the security
checklist in Architecture.md (Section 12). Cover: login and token verification, role permissions
per endpoint, input validation, password handling (confirm nothing is stored or logged
locally, since Clerk owns credentials), database access (SQL injection, least-privilege
DB user), secrets (code and git history), dependencies, and deployment settings.

Output a table: finding | location | severity | how to reproduce | recommended fix.
Do not change any code. Wait for me to approve a fix list.
```

**Prompt 5B: Fix and verify**
```
Fix the approved findings in order of severity. For each fix, add or update a test that
would have caught it, and tell me how to verify it manually. Provide a suggested commit
message per fix.
```

**Prompt 5C: Endpoint permission matrix**
```
Generate a role-by-endpoint permission matrix (employee, staff, admin, unauthenticated)
from the actual routes, then write tests that assert every cell of the matrix.
Flag any endpoint whose behavior differs from Architecture.md.
```

---

## Week 6: Polish

**Goal:** A smooth, mobile-friendly UI, with errors tracked and workflows tested across browsers.

**Exit criteria**
- [ ] Navigation is consistent and role-appropriate
- [ ] Forms have clear labels, inline validation, and helpful error messages
- [ ] Layout works at phone, tablet, and desktop widths
- [ ] Sentry capturing errors from React and FastAPI, with personal data scrubbed
- [ ] BrowserStack run completed for the main workflows, results recorded
- [ ] Code quality pass completed across the whole codebase
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 6A: UX review**
```
Week 6, Polish. Review the React app for navigation, form usability, error messages,
empty states, loading states, and mobile layout. Report issues in a table:
page | issue | severity | suggested fix. Do not change code yet. Wait for my selection.
```

**Prompt 6B: Implement polish**
```
Implement the approved polish items. Keep changes small and grouped by page.
Replace generic error messages with specific, actionable ones that map to the API's
error codes. Plan first, wait for approval.
```

**Prompt 6C: Sentry**
```
Integrate Sentry in React and FastAPI. Use environment-based DSNs from .env,
scrub tokens and personal data before sending, and tag events with environment and
release. Explain how to trigger a test error in each app and where to see it.
```

**Prompt 6D: BrowserStack test plan**
```
Create a BrowserStack test matrix for these workflows: submit a ticket, assign and
resolve a ticket, add an asset. Include browsers and devices (at least one iOS,
one Android, and the latest Chrome, Firefox, Safari, and Edge), the exact steps,
expected results, and a table for recording actual results with date.
```

**Prompt 6E: Code quality pass**
```
Week 6, Code quality pass. Review the whole codebase against Rules.md section 8
(code cleanliness): function and file size, duplication, naming conventions, magic numbers
and strings, unused code, import order, and leftover debug output.

Report findings in a table: file | issue | rule | suggested fix. Do not change any code yet.
Wait for me to pick which to fix. Then fix them in small changes I can commit one at a time as refactor: commits, and confirm that
tests, ruff, ESLint, and Prettier all pass.
```

---

## Week 7: Deploy

**Goal:** A live, working deployment with a repository others can set up from the README.

**Exit criteria**
- [ ] Deployed to Azure or Heroku with production environment variables
- [ ] Production database migrated; seed data limited to fake demo data
- [ ] Clerk production keys configured and allowed origins set
- [ ] README has setup instructions, screenshots, and a demo guide
- [ ] Smoke test of all three core workflows on the live site
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 7A: Choose the platform**
```
Week 7, Deploy. Compare Azure and Heroku for this stack: Docker support, PostgreSQL
hosting, how the frontend and API would be served, student-credit cost, and effort.
Recommend one. Note that Heroku does not run Docker Compose files directly.
Give me a deployment outline and a rollback plan. Do not deploy anything yet.
```

**Prompt 7B: Production configuration**
```
Prepare production configuration for the chosen platform: production Dockerfiles or
buildpack setup, environment variable list (names only, no values), CORS and Clerk
settings, the Alembic migration step on deploy, the production server command
(uvicorn, or gunicorn with uvicorn workers), whether /docs stays exposed, and a
post-deploy smoke test checklist.
Plan first, wait for approval.
```

**Prompt 7C: Repository presentation**
```
Write the repository README: project overview, features by role, architecture diagram,
tech stack, local setup with docker compose, environment variables table, deployment
notes, a screenshot placeholder list, and a demo guide with a step-by-step script
using the seeded demo accounts. Keep it clear and scannable.
```

---

## Week 8: Optional enhancement (Ticket priorities and SLA dashboard)

**Goal:** Priority levels, due dates, and a dashboard of overdue tickets.

**Exit criteria**
- [ ] Priority (for example low, medium, high, urgent) selectable on tickets
- [ ] Due date set automatically from a priority-based SLA policy and editable by staff
- [ ] "Overdue" defined clearly (due date passed and status not resolved or closed)
- [ ] Dashboard shows overdue tickets and counts by priority
- [ ] Migration, tests, and docs updated
- [ ] Review and Polish run; code-quality findings fixed (Rules.md section 8)

**Prompt 8A: Design the enhancement**
```
Week 8, Optional Enhancement. Design ticket priorities and SLA due dates on top of the
existing schema. Specify the migration, the SLA policy (priority to hours, in config),
how overdue is calculated, API changes, and UI changes. Keep it simple: no business-hours
calendars. Do not write code. Wait for approval.
```

**Prompt 8B: Build and verify**
```
Implement the approved SLA design: migration, backend logic, endpoints, React priority
selector and due date display, and the overdue dashboard in the Report module.
Include tests for overdue edge cases (due exactly now, resolved late, no due date).
Update the README and the manual.
```

---

## Documentation track (spread across Weeks 6-8)

Start drafts early and finalize after Week 6 polish so screenshots match the final UI.

**Prompt D1: User manual**
```
Write the user manual with three step-by-step guides: (1) submit a ticket,
(2) assign and resolve a ticket, (3) add an asset. For each guide use this template:
Purpose, Required role, Prerequisites, Numbered steps, Expected result.
Mark where a screenshot belongs with [SCREENSHOT: filename-description].
Use plain language for non-technical readers.
```

**Prompt D2: Workflow diagram**
```
Create a Mermaid swimlane-style flowchart with lanes for Employee and Staff showing:
ticket submission, staff assignment, status updates, and resolution, including user and
staff actions and the allowed status transitions. Add a short legend and a text
walk-through of the diagram below it.
```

**Prompt D3: Screenshots and testing record**
```
Create (1) a screenshot checklist listing every shot needed for the manual and README,
with filename, page, role, and what data should be visible, and (2) a testing record
template and filled-in rows for each workflow: workflow | steps | expected | actual |
browser/device | date | tester. Leave "actual" and "date" blank for me to complete.
```
