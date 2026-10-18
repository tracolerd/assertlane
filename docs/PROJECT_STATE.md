# AssertLane - Project State
## Mission
Small engineering team-এর জন্য projects, test suites, cases, manual/automated executions, failure evidence এবং release-readiness criteria ম্যানেজ করার একটি traceable quality-engineering product।
## Current Phase: Phase 2 (Project CRUD API)
- [x] Phase 0: Environment inspection and requirement verification.
- [x] Phase 1: Backend project setup, SQLite integration, Alembic migrations, and core models.
- [ ] Phase 2: Project/suite/test-case CRUD APIs and basic frontend list/forms.
## Known Risks & Blockers
- Target Architecture requires PostgreSQL; ORM (SQLAlchemy) must be database-agnostic. Currently using SQLite for MVP.
## Next Milestone
Implement FastAPI CRUD endpoints for Project entity and write API integration tests.
