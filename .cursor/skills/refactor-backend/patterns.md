# Backend Refactoring Patterns

Recipes for common structural improvements. Each pattern is one step — combine across multiple PRs, not one diff.

## Extract Service from Handler

**When:** Route/controller contains business rules, external API calls, or multi-step orchestration.

**Steps:**
1. Create `services/<domain>.py` (or match existing folder convention).
2. Move logic into a function/class method with explicit inputs and return type.
3. Replace handler body with: validate input → call service → map to response.
4. Pass dependencies explicitly (db session, config, clients) — match how the repo already injects deps.

**Handler after:**
```python
@router.post("/stories")
def create_story(body: StoryCreate, session: Session = Depends(get_session)):
    story = story_service.create(session, body)
    return story
```

**Keep in handler:** HTTP concerns only — status codes, headers, request/response models, auth decorators.

---

## Consolidate Exception Handlers

**When:** Repeated try/except blocks or duplicate error JSON shapes across routes.

**Steps:**
1. Define domain exceptions in one module (if not already).
2. Register handlers on the app/framework exception registry.
3. Remove per-route catch blocks that only re-wrap the same response.
4. Verify status codes and response body shape match previous behavior exactly.

**FastAPI:** `@app.exception_handler(DomainError)` in `main.py` or a dedicated `exceptions/handlers.py` imported at startup.

**Express/Nest:** Global error middleware or `@Catch()` filter.

---

## Split Fat Router

**When:** One router file owns unrelated endpoints or exceeds ~200 lines.

**Steps:**
1. Group endpoints by domain (auth, stories, jobs).
2. Create one router module per domain.
3. Move shared dependencies to a `deps.py` or existing DI module.
4. Register routers in the entry point with the same URL prefixes as before.

**Rule:** URL paths and HTTP methods must not change unless the user approves breaking changes.

---

## Introduce Repository Layer

**When:** SQL/ORM queries are scattered across services or handlers.

**Steps:**
1. Create `repositories/<entity>.py` with query methods (`get_by_id`, `list_for_user`, etc.).
2. Move raw queries from services into repository methods.
3. Services call repositories; repositories know nothing about HTTP.

**Skip when:** The project already uses an active-record pattern consistently and the refactor goal doesn't include data-access isolation.

---

## Extract Shared Response/Error Builders

**When:** Same JSON error envelope built inline in many places.

**Steps:**
1. Find the canonical error shape already used by clients.
2. Add one helper (e.g. `error_response(code, message)`) where similar helpers live.
3. Replace inline dict construction call sites one file at a time.

---

## Module Reorganization

**When:** Flat or confusing folder layout (`utils.py` with everything).

**Target layout (adapt to stack):

```
backend/
├── main.py              # app factory, router registration, lifespan
├── core/                # config, shared clients, constants
├── routers/             # HTTP layer (thin)
├── services/            # business logic
├── repositories/        # data access (optional)
├── models/              # DB/schema models
├── schemas/             # request/response DTOs (if separated from ORM)
└── exceptions/          # domain errors + handlers
```

**Steps:**
1. Create target directories.
2. Move one module at a time; fix imports; run tests.
3. Avoid renaming public symbols during the move — move first, rename later if needed.

---

## Dependency Injection Cleanup

**When:** Config or clients are imported as globals inside business logic.

**Steps:**
1. Identify what's already injected via framework DI (`Depends`, middleware, context).
2. Thread dependencies through constructors or function parameters.
3. Remove module-level side effects where possible (client init at import time).

---

## Remove Dead Code

**When:** Unused routes, models, or imports after extraction.

**Steps:**
1. Search for references across the repo (not just the backend folder if monorepo).
2. Delete unused symbols; remove from router registration.
3. Check OpenAPI/docs for orphaned endpoints.

**Caution:** Confirm nothing is called from scripts, cron jobs, or frontend before deleting.

---

## Database Model Refactor

**When:** Splitting tables, renaming columns, or normalizing relations.

**Always separate from structural refactor:**
1. Add migration (Alembic, Prisma migrate, etc.).
2. Deploy migration.
3. Update application code to use new schema.

Never rename DB columns and reorganize service layers in the same step without explicit user approval.

---

## Testing Strategy During Refactor

| Coverage | Strategy |
|----------|----------|
| Good unit/integration tests | Refactor aggressively; tests are the safety net |
| Thin coverage | Add tests for the module being refactored first |
| None | Manual smoke script + smallest possible steps |

Prefer characterization tests (assert current output) over rewriting tests to match new structure mid-refactor.
