# Backend Refactor Checklist

Run before marking a refactor step or PR complete.

## Behavior

- [ ] Public API unchanged (paths, methods, request/response shapes, status codes)
- [ ] Auth and authorization behavior unchanged
- [ ] Error messages and codes match previous contract (or user approved changes)
- [ ] Background jobs, webhooks, and event handlers still wired correctly

## Code Quality

- [ ] Handlers/routes are thin — no business logic left inline unless intentional
- [ ] No circular imports introduced
- [ ] Imports updated; no orphaned modules
- [ ] Naming matches project conventions
- [ ] No new generic abstractions without at least two concrete uses

## Verification

- [ ] Tests pass (command documented in PR/summary)
- [ ] Linter/type-check pass if project uses them
- [ ] Critical endpoints smoke-tested when test coverage is low
- [ ] OpenAPI/Swagger still generates if applicable

## Scope Discipline

- [ ] Diff limited to refactor goal — no feature additions
- [ ] No unrelated formatting churn across untouched files
- [ ] Config/secrets not modified unless required
- [ ] DB migrations in separate change if schema changed

## Documentation

- [ ] Summary explains what moved and why
- [ ] Follow-up debt called out explicitly
- [ ] Breaking changes flagged prominently (should be rare)
