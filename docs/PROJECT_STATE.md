# AssertLane - Project State
## Mission
Small engineering team-এর জন্য projects, test suites, cases, manual/automated executions, failure evidence এবং release-readiness criteria ম্যানেজ করার একটি traceable quality-engineering product।
## Current Phase: Phase 3 (TestSuite and TestCase CRUD)
- [x] Phase 0: Environment inspection and requirement verification.
- [x] Phase 1: Backend project setup, SQLite integration, Alembic migrations, and core models.
- [x] Phase 2: Project CRUD APIs and automated tests.
- [ ] Phase 3: TestSuite and TestCase (with versioning snapshot) CRUD APIs.
## Known Risks & Blockers
- Target Architecture requires PostgreSQL; ORM (SQLAlchemy) must be database-agnostic. Currently using SQLite for MVP.
## Next Milestone
Define TestSuite and TestCase models, generate migrations, and implement their API endpoints.
