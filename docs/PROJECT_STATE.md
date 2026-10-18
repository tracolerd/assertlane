# AssertLane - Project State
## Mission
Small engineering team-এর জন্য projects, test suites, cases, manual/automated executions, failure evidence এবং release-readiness criteria ম্যানেজ করার একটি traceable quality-engineering product।
## Current Phase: Phase 7 (Frontend Dashboard & MVP Complete)
- [x] Phase 0: Environment inspection and requirement verification.
- [x] Phase 1: Backend project setup, SQLite integration, Alembic migrations, and core models.
- [x] Phase 2: Project CRUD APIs and automated tests.
- [x] Phase 3: TestSuite and TestCase APIs and tests.
- [x] Phase 4: Manual test run lifecycle APIs and tests.
- [x] Phase 5: Result import endpoint implemented and tested.
- [x] Phase 6: Repository-controlled Playwright test runner and custom JSON integration script implemented.
- [x] Phase 7: React + TypeScript + Tailwind CSS Frontend Dashboard implemented and integrated with FastAPI.
## Known Risks & Blockers
- The current React UI calls `http://127.0.0.1:8000` directly. In the hosted Netlify page, that address resolves to the visitor's own device; the public UI is not connected to a hosted API.
- FastAPI routes do not yet enforce authentication or authorization.
- No explicit CORS policy is configured in the backend.
- SQLite is configured with a local relative file path; production database configuration and a durable backend deployment are not complete.
- Test-result creation does not verify that the test case and test run belong to the same project.
- Result records store the test-case version number but not a complete immutable case-definition snapshot; cascade deletes can remove results.
- The repository has no committed GitHub Actions workflow. `automation/package.json` still has a placeholder `npm test` command that exits with an error.
- Current tests use a shared relative `test.db` without consistent cleanup/isolation.
- See [Release Readiness Audit](RELEASE_AUDIT.md) for source evidence and prioritized remediation.

## Next Milestone
Future enhancements (e.g., Suite/Case management UI views, test execution runners in UI).
