# Prioritized Engineering Backlog

These candidates reflect the current documented AssertLane MVP. Validate each against the source and existing tests before treating it as a reproduced defect.

## Candidate issues

1. **Add authentication and resource authorization** — Protect every API route and verify that a caller can access only projects, suites, cases, runs, and results they are authorized to manage before any public deployment.
2. **Configure the frontend API origin by environment** — Remove the hard-coded loopback address and define safe local/staging/production configuration with a clear missing-configuration error.
3. **Add an explicit CORS allowlist** — Permit only intended frontend origins and document that CORS is not a replacement for authentication.
4. **Enforce project/run/case relationship integrity** — Reject imported or directly created results when the test case does not belong to the project associated with the run.
5. **Preserve immutable historical test-case definitions** — Store a reconstructable snapshot or immutable revision reference with each result, not only a version number.
6. **Isolate the test database per test run** — Use a temporary database/session fixture and prove tests are order-independent and clean up their state.
7. **Bound and validate report imports** — Limit batch size and field lengths, validate every entry, and return per-row errors without leaking internal exceptions.
8. **Enforce a legal test-run state machine** — Define allowed transitions and reject invalid status changes consistently at the service layer.
9. **Replace the placeholder npm test command and add CI** — Run real backend tests, frontend checks/build, and a reproducible Playwright smoke test in automation.
10. **Replace nullable update fields with explicit PATCH semantics** — Ensure explicit null is rejected for non-nullable fields while omitted fields remain unchanged.

## Suggested order

Security and ownership (1–4) come first, followed by historical integrity and test reliability (5–8), then CI and API contract polish (9–10). Do not describe the hosted frontend as a complete full-stack deployment until the browser-to-API path is verified.
