# Architecture Decisions Log
## 001. Local Development Database (MVP)
**Context:** The target architecture uses PostgreSQL, but local development environments may lack Docker or dedicated database servers.
**Decision:** Use SQLite for local development and MVP phases. We will use SQLAlchemy as the ORM to ensure seamless migration to PostgreSQL by simply changing the database URL in the .env file.
**Consequences:** Simplifies onboarding and avoids infrastructure setup overhead. Some PostgreSQL-specific features (like JSONB specific operators) must be avoided or abstracted during MVP.
## 002. Execution Records Immutability
**Context:** Modifying old test cases can implicitly invalidate past test results.
**Decision:** Implement a lightweight snapshotting/versioning strategy for TestCase entities. Test executions (TestResult) will strictly append data and reference a specific TestCase version to prevent historical rewrite.
