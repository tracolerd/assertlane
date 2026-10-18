# AssertLane — Release Readiness Audit

**Audit date:** 2026-10-18  
**Branch reviewed:** `main`  
**Scope:** Static source/configuration review of the repository and its test/deployment wiring.  
**Not performed:** No code was executed, no pytest or Playwright suite was run, no penetration test was performed, and the hosted Netlify page could not be independently loaded through the available audit browsing path. Findings about deployment behavior are based on the committed source and configuration.

## Executive decision

**NO-GO for a publicly exposed, multi-user API or production use with real test data.** A public frontend preview is acceptable if clearly labelled as a preview and users are warned that the current browser-to-API integration is not deployment-ready.

The repository is beyond a planning-only scaffold: it contains CRUD API routes, relational models, migration files, test modules, a small React interface, and one Playwright demo test. However, several integration and security requirements remain incomplete.

## Findings

### A-01 — Critical before public API exposure: no authentication or authorization

**Evidence:** `backend/main.py` defines project, suite, case, run and result read/write/delete routes without a user identity or permission dependency.

**Impact:** Any client that can reach the API can access and mutate the same application records. This is not safe for confidential test plans, credentials embedded in notes, or multi-user use.

**Recommendation:** Add authentication and resource-level authorization. Every resource query and mutation must prove ownership/permission; do not rely on hiding actions in the UI. Add tests for unauthenticated requests, role boundaries and cross-project access.

### A-02 — High: deployed browser calls a loopback API address

**Evidence:** `frontend/src/App.tsx` calls `http://127.0.0.1:8000/api/health` and `http://127.0.0.1:8000/api/projects/` directly.

**Impact:** In a browser opened at the Netlify URL, `127.0.0.1` refers to the visitor's own device, not an AssertLane server. Publishing the frontend does not publish the FastAPI backend.

**Recommendation:** Provide a validated, environment-driven API base URL and deploy the backend separately before advertising end-to-end live functionality.

### A-03 — High: no explicit CORS policy

**Evidence:** `backend/main.py` creates the FastAPI app without CORS middleware; the frontend uses a different origin/port in local development and a different origin on Netlify.

**Impact:** Browser requests from the frontend origin are expected to be blocked by the browser unless an appropriate CORS policy is added.

**Recommendation:** Configure an explicit allowlist for known development and production origins. Do not use a wildcard origin as a shortcut for a credentialed application.

### A-04 — High: local-only database configuration

**Evidence:** `backend/database.py` hard-codes `sqlite:///./assertlane.db`; `backend/alembic.ini` also declares a local SQLite URL. No environment-driven database URL or backend deployment configuration is committed.

**Impact:** The current setup is designed around a local file, not durable, monitored production storage. Ephemeral server filesystems and multiple backend instances require a different design.

**Recommendation:** Load the database URL from deployment configuration, choose a supported persistent database, and test migrations/backup/restore on the target hosting platform.

### A-05 — High: result creation does not validate project consistency

**Evidence:** `POST /api/runs/{run_id}/results/` confirms that the run exists, while the CRUD layer independently checks that a test case exists. It does not verify that the case's suite/project matches the run's project.

**Impact:** A result can be recorded against a run and an unrelated test case, weakening traceability and release evidence.

**Recommendation:** Resolve the run and case relationships within one validated operation, reject mismatched project ownership, and cover the negative path in integration tests.

### A-06 — High: historical test-case evidence is not fully immutable

**Evidence:** `TestResult` stores `test_case_version`, while updates mutate the existing `TestCase`. There is no separate revision record or complete definition snapshot. The `TestCase` and `TestRun` relationships configure cascades that can delete their associated results.

**Impact:** A version number alone cannot reconstruct a historical test definition, and deleting a case/run can remove evidence.

**Recommendation:** Choose and document an explicit retention policy. Store full case revisions/snapshots referenced by results, and separate archive/deactivation from destructive deletion when historical evidence must be retained.

### A-07 — High: automation wiring is local-only and failure handling is weak

**Evidence:** `automation/playwright.config.ts` uses `http://127.0.0.1:8000`; `automation/push_results.js` posts to the same loopback address. The bridge logs caught errors and does not enforce a successful HTTP response before finishing.

**Impact:** This does not work as a remote CI reporter without changes, and upload failure may not be surfaced as a reliable process failure.

**Recommendation:** Configure the target API URL, secure the reporter with scoped credentials, validate HTTP status and response schema, fail non-zero on upload errors, and add tests for failed/time-out uploads.

### A-08 — High: no repository CI workflow; npm test script is a placeholder

**Evidence:** The default branch tree contains no `.github/workflows/` workflow. `automation/package.json` defines `test` as an echo followed by `exit 1`.

**Impact:** There is no repository CI evidence for this branch, and `npm test` is expected to fail by design. A Playwright config does not mean Playwright is automatically run.

**Recommendation:** Replace the placeholder script with the intended Playwright command, add a real CI workflow with an isolated database, run migrations and backend tests, then run frontend build/lint and Playwright.

### A-09 — Medium: tests share a persistent local test database

**Evidence:** Test modules use `sqlite:///./test.db` and run `Base.metadata.create_all` without a suite-wide cleanup/reset strategy.

**Impact:** Records can persist between runs and tests can affect one another. This weakens repeatability and can hide ordering assumptions.

**Recommendation:** Use a dedicated temporary database or transaction/fixture rollback; clear dependency overrides during teardown, and verify tests run independently and in randomized order.

### A-10 — Medium: request and lifecycle validation is incomplete

**Evidence:** List endpoints accept `skip` and `limit` without explicit range constraints. Bulk import has no maximum result count. Update schemas permit explicit `null` for some fields that map to non-null database columns. Run status updates do not enforce a legal state-transition graph.

**Impact:** Oversized requests, invalid pagination, integrity errors and nonsensical status transitions are insufficiently controlled.

**Recommendation:** Apply Pydantic and query bounds, constrain batch sizes and duration fields, return predictable 4xx errors, and implement/test valid state transitions.

### A-11 — Medium: frontend scope and HTML metadata remain starter-level

**Evidence:** `frontend/src/App.tsx` currently only creates/lists projects and shows API status. `frontend/index.html` still uses the generic title `frontend`; `frontend/README.md` is the default Vite template.

**Impact:** The published UI does not present the complete API workflow and still contains starter-project branding.

**Recommendation:** Build suite/case/run/result views after backend connectivity is corrected; update document title, favicon/metadata and nested documentation to match the actual product.

## Positive evidence

- The core project/suite/case/run/result API routes are implemented.
- SQLAlchemy models and Alembic migration files exist.
- Four backend pytest modules cover basic CRUD and report import paths.
- The Playwright configuration emits a JSON report and the demo test targets a controlled `/demo` route.
- The result schema distinguishes `Error` from `Failed`, which is useful for separating environment/automation problems from product assertions.

This positive evidence is evidence of implementation in source—not proof that tests currently pass or that the hosted app is fully integrated.

## Release checklist

- [ ] Deploy a persistent backend with environment-driven database configuration.
- [ ] Configure the frontend API origin and explicit CORS allowlist.
- [ ] Add authentication and resource-level authorization.
- [ ] Enforce same-project relationships for run/case results.
- [ ] Preserve reconstructable historical case definitions and define deletion/retention semantics.
- [ ] Validate API inputs, pagination, batch sizes and run-state transitions.
- [ ] Isolate tests and make `npm test` meaningful.
- [ ] Add CI and verify backend tests, frontend build/lint and Playwright end-to-end tests.
- [ ] Perform a black-box smoke test against the published Netlify page and deployed API.
- [ ] Replace the generic page title and starter template documentation.

**Audit outcome:** Keep AssertLane labelled as an MVP/frontend preview until the high-severity items are closed and a deployed end-to-end check provides evidence.
