# Week 1: Decisions Log entries

Draft rows for section 19 of `system-architecture/Architecture.md`. The assistant does not edit that folder, so paste them in yourself. Each row uses the log's columns: decision, chosen, rejected, reason.

## Dependencies approved in Week 1

| Decision | Chosen | Rejected | Reason |
|---|---|---|---|
| Frontend build plugin | `@vitejs/plugin-react` (dev) | Writing the JSX transform by hand | Vite's official React transform |
| Tailwind integration | `@tailwindcss/vite` (dev) with Tailwind v4 | Tailwind v3 with `postcss` and `autoprefixer` | Fewer packages and the official v4 path |
| ESLint rule sets | `@eslint/js`, `eslint-plugin-react`, `eslint-plugin-react-hooks`, `globals` (dev) | ESLint core rules alone | Catches React and hook mistakes |
| ESLint and Prettier together | `eslint-config-prettier` (dev) | Letting both tools enforce formatting | Prevents rule conflicts |
| Test DOM | `jsdom` (dev) | `happy-dom` | Standard Vitest and Testing Library setup |

## Deviations and implementation decisions

| Decision | Chosen | Rejected | Reason |
|---|---|---|---|
| ESLint version | 9.39.5 | ESLint 10 | `eslint-plugin-react` does not support 10 yet. A Dependabot ignore is planned for Week 5 |
| Clerk SDK patch | `@clerk/clerk-react` 5.61.10 | 5.61.3 | A high-severity advisory is fixed in 5.61.10. The move to `@clerk/react` is a separate Week 2 decision |
| Dev requirements | `backend/requirements-dev.txt` | One file for runtime and dev | Keeps dev tools out of the production image |
| Health route | `core/health.py`, mounted in `main.py` | Inline route in `main.py` | Keeps routers thin and gives the route a testable home |
| Line endings | `.gitattributes` forcing LF | Platform defaults | Docker, shell scripts, and Prettier behave the same on every OS |
| Test cleanup | `frontend/vitest.setup.js` runs `cleanup` after each test | Vitest globals mode | Avoids global test functions and extra ESLint config |
| Prettier scope | `frontend/.prettierignore` (dist, node_modules, lockfile) | Formatting every file | Generated files should not be reformatted |
| Extra ruff rules | `ANN` and `T20` on top of the minimum set | The minimum set only | Enforces type hints and bans `print`, per Rules.md section 8 |
| Settings default | `ENVIRONMENT` defaults to production, `extra="ignore"` | Defaulting to development | A missing variable never exposes `/docs` |
| App construction | `create_app(settings)` plus a module-level `app` | Only a module-level app | Tests build apps with chosen settings |
| Container names | `desktrack_db`, `desktrack_backend`, `desktrack_frontend`, with service names unchanged | Renaming the services | Readable names in Docker Desktop while the service names in Architecture.md stay valid |
| `pyjwt[crypto]` | Added in Week 2 | Added in Week 1 | Unused until token verification |
| Pre-commit frontend hooks | Local hooks calling tools in `frontend/node_modules` | `mirrors-prettier` and ESLint mirrors | Same tool versions as CI, and the mirrors are archived |

## Added by the Week 1 code-quality fixes

| Decision | Chosen | Rejected | Reason |
|---|---|---|---|
| Python pins | Every package pinned, including transitive ones, using `pip freeze` inside `python:3.12.15-slim` | Pinning direct packages only, or adding `pip-tools` | Reproducible builds without a new tool |
| `uvloop` pin | Marker `; sys_platform != "win32"` | A bare pin | `uvloop` does not install on Windows |
| Dependency audit | `pip-audit --no-deps -r requirements.txt` | Letting `pip-audit` resolve dependencies again | Audits exactly the pinned set |
| Error codes | `METHOD_NOT_ALLOWED` (405) added to the Architecture.md code list | Leaving 405 on FastAPI's default format | One error format for every response |
| Error envelope | `ErrorCode`, `AppError`, and four handlers in `core/exceptions.py` | Handling errors per route | Unknown routes, validation errors, and crashes all use the shared envelope |
| Error models location | Error models live in `core/exceptions.py` | Putting them in `core/responses.py` | Avoids a circular import with `ErrorCode` |
| Validation details | `[{field, message}]` with a dotted path such as `body.title` or `query.page`, and no echoed input | FastAPI's default, which includes the submitted input | Submitted input could contain secrets |
| Unhandled errors | Generic 500 body, with no exception text | Returning the exception message | Avoids leaking internals |
| Database URL type | `SecretStr` | Plain `str` | Keeps the password out of `repr()` and logs |
| Dev ports | `127.0.0.1:8000` and `127.0.0.1:5173` | Binding to all interfaces | Only your machine can reach the dev servers |
| Documentation folder | `docs/weekly/` | Adding notes under existing `docs/` folders | Per-week notes need a home, and Architecture.md section 16 does not list one |

## Edits to make in the reference files

- **Architecture.md section 5:** add `METHOD_NOT_ALLOWED` (405) to the error code list.
- **Architecture.md section 4:** note that Python dependencies are fully pinned, and that `pyjwt[crypto]` arrives in Week 2.
- **Architecture.md section 16:** add `docs/weekly/` to the repository tree.
- **Rules.md section 4:** add 405 to the list of status codes.
