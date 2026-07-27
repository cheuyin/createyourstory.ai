---
name: refactor-backend
description: >-
  Refactors backend code safely in incremental steps: restructure modules,
  extract services, consolidate handlers, improve layering, and reduce coupling
  without breaking API contracts. Use when refactoring a backend, restructuring
  API/server code, extracting services or repositories, reorganizing routes,
  cleaning up handlers or models, or when the user mentions backend refactor,
  tech debt, or module reorganization.
---

# Refactor Backend

Refactor backend code by preserving behavior first, then improving structure. Never mix behavior changes with structural changes in the same step.

## Before You Start

1. **Clarify the goal** — Ask only if unclear:
   - What pain point? (fat handlers, duplicated logic, tangled deps, hard to test)
   - Any constraints? (no API breaks, no schema migration, deadline)
   - Scope? (one module, one layer, whole backend)

2. **Map the backend** — Read before editing:
   - Entry point (`main.py`, `app.ts`, `server.js`, etc.)
   - Route/controller layer
   - Service/business logic
   - Data access (ORM models, repositories, queries)
   - Config, exceptions, middleware, auth
   - Test layout and how to run them

3. **Establish a baseline** — Run existing tests and note the command. If no tests exist, identify critical endpoints or flows to smoke-check manually after each step.

## Refactoring Principles

- **One concern per change** — Extract a service OR move files OR rename types; not all at once.
- **Behavior-preserving steps** — Each commit-sized step should pass tests and keep public API identical unless the user explicitly allows breaking changes.
- **Follow existing conventions** — Match naming, folder layout, error shapes, dependency injection style, and import patterns already in the repo.
- **Minimize diff scope** — Do not rewrite unrelated code, add features, or "improve" things outside the refactor goal.
- **Prefer composition over new abstractions** — Extract only when duplication or coupling justifies it; avoid premature layers.

## Workflow

Copy and track progress:

```
Refactor progress:
- [ ] Step 0: Map structure + run baseline tests
- [ ] Step 1: Plan incremental steps (ordered, smallest first)
- [ ] Step 2: Execute step N (one concern)
- [ ] Step 3: Verify (tests, lint, smoke critical paths)
- [ ] Step 4: Repeat until goal met
- [ ] Step 5: Summarize changes and remaining debt
```

### Step 0: Map structure

Produce a brief mental model (do not dump a huge tree unless asked):

| Layer | Location | Notes |
|-------|----------|-------|
| Entry | | |
| Routes/controllers | | |
| Services | | |
| Data/models | | |
| Cross-cutting | auth, exceptions, config | |

Flag coupling hotspots: handlers doing DB + business logic + external API calls in one function.

### Step 1: Plan incremental steps

Order steps so each is independently verifiable:

1. **Preparatory** — Add tests for untested critical paths (only if needed for safety).
2. **Extract without moving** — Pull logic into functions/classes in the same file.
3. **Move to new module** — Relocate extracted code; update imports.
4. **Consolidate duplicates** — Merge repeated patterns (error handlers, response builders).
5. **Thin the outer layer** — Routes/controllers delegate to services only.
6. **Clean up** — Remove dead code, fix imports, delete unused deps.

For large refactors spanning many files, suggest splitting into reviewable PRs (see `/split-to-prs`).

### Step 2: Execute one step

For each step:

1. State what moves/changes and what stays the same.
2. Make the smallest diff that achieves the step.
3. Update all call sites and imports in the same step — no broken intermediate state.
4. Keep error response shapes, status codes, and request/response schemas unchanged unless explicitly requested.

### Step 3: Verify

After every step:

```bash
# Adapt to project — discover from pyproject.toml, package.json, Makefile, etc.
# Python/FastAPI example:
cd backend && uv run pytest
cd backend && uv run ruff check .

# Node example:
npm test && npm run lint
```

If tests fail:
- Fix regressions before proceeding.
- If a failure reveals a pre-existing bug unrelated to the refactor, note it and ask whether to fix separately.

Smoke-check critical flows when test coverage is thin:
- Auth login/token validation
- Primary CRUD or job-processing endpoints
- Error paths (404, 401, validation errors)

### Step 4: Repeat or stop

Stop when the stated goal is met. Report:
- What improved (layering, file count, duplication removed)
- What was intentionally left alone
- Residual tech debt or follow-up refactors

## Common Refactor Patterns

See [patterns.md](patterns.md) for layer-by-layer recipes (extract service, consolidate exception handlers, split fat router, repository extraction).

Choose the pattern that matches the goal; do not apply all patterns in one pass.

## Decision Guide

| Situation | Approach |
|-----------|----------|
| Handler > ~40 lines with mixed concerns | Extract service method; handler orchestrates only |
| Duplicate error handling across routes | Consolidate into middleware or registered exception handlers |
| Business logic in ORM models | Move to service; keep models as data shape only |
| Circular imports after extraction | Introduce a thin interfaces/types module or reorder dependencies (data ← service ← route) |
| Need DB schema change | Separate migration PR from structural refactor |
| No tests, high risk | Add characterization tests first or refactor in tiny steps with manual smoke checks |
| Refactor touches >10 files | Plan PR splits by layer or feature slice |

## Anti-Patterns

- Big-bang rewrite of a module in one diff
- Renaming public API fields or routes without user approval
- Adding new frameworks or ORMs mid-refactor
- Changing behavior "while we're here"
- Creating generic base classes or factories for one use case
- Moving files without updating imports in the same commit

## Output Format

When reporting refactor progress to the user:

```markdown
## Refactor: [goal]

### Done this step
- [Concrete change with file references]

### Verification
- Tests: pass/fail (+ command run)
- Manual checks: [if any]

### Next step
- [Single next action, or "complete"]

### Notes
- [Breaking-change risks, follow-ups, debt left intentionally]
```

## Additional Resources

- Layer-specific recipes: [patterns.md](patterns.md)
- Pre-merge checklist: [checklist.md](checklist.md)
