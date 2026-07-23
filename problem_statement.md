# ApplyTrack — Problem Statement

## What I'm building

I'm building a backend API to track my own job application pipeline, companies I've applied to, the specific roles under each company, and every interview round tied to a given application, from OA through offer or rejection.

This is a from-scratch project. No course, no follow-along, no reference implementation open in a side window. I've completed a JWT-authenticated Todo API as a guided course project before this, and this build exists specifically to test how much of that actually stuck when there's no instructor's code to lean on.

*If you're interested in the previous project (a follow-along with a course):*

**Todo API App** → [`02_FastAPI_Fundamentals/06_Todo_API_with_JWT_Authentication`](https://github.com/saddab-ansari/Backend-Architecture/tree/main/02_FastAPI_Fundamentals/06_Todo_API_with_JWT_Authentication)

## Tech stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Auth:** JWT (`python-jose`), OAuth2 password flow
- **Password hashing:** `passlib` (bcrypt)
- **Config:** `.env` via `python-dotenv` — no hardcoded secrets in source

## Data model

Three entities, chained under a user:

```
User
 └── Company        (a company I'm applying to)
       └── Application   (a specific role at that company)
             └── InterviewRound  (one or more rounds tied to one application)
```

- Every `Company` belongs to exactly one user.
- Every `Application` belongs to exactly one `Company` and one user — all data is scoped to the logged-in user's own records.
- Every `Application` carries a single `status` field (`wishlist`, `applied`, `oa`, `interviewing`, `offer`, `rejected`, `withdrawn`) that I update independently of its rounds.
- Every `Application` owns a list of `InterviewRound` rows — each with its own type, scheduled date, and outcome. An application's status doesn't auto-derive from its rounds; I set it explicitly.

## Core features

1. **Auth** — register, log in, receive a JWT. Reused pattern from the Todo API, but with the secret key moved out of source code into `.env`.
2. **Company CRUD** — full create/read/update/delete, scoped to the logged-in user.
3. **Application CRUD** — full CRUD, linked to a company, scoped to the logged-in user.
4. **Status transitions** — a dedicated `PATCH /applications/{id}/status` endpoint that updates only the status field, instead of overloading a full-object `PUT` for a single-field change.
5. **Interview rounds** — CRUD for rounds nested under a specific application. Fetching a single application returns it with its rounds included, using a SQLAlchemy `relationship()` instead of a manual second query.
6. **Filtering, sorting, pagination** — `GET /applications` supports filtering by status, sorting by applied date, and `skip`/`limit` pagination.
7. **Dashboard** — `GET /dashboard/stats` returns application counts grouped by status, using SQLAlchemy's `func.count()` and `group_by()`.

## Stretch goals

- Alembic migrations instead of `create_all()`.
- A handful of `pytest` tests covering the auth flow and one CRUD resource.
- An admin endpoint to view all users' applications, reusing the role-check pattern from the Todo API's admin router.

## Constraints I'm holding myself to

- No copying code directly from the Todo API's files — same patterns, re-derived from memory and docs, not pasted.
- Every route, model field, and design decision here is mine to justify — nothing inherited from a course's structure by default.
- Secrets stay out of source control from the first commit.
- Commits happen incrementally as features land, not as one bulk dump at the end — the commit history is part of the point.

## What "done" looks like

All core features above working end-to-end, testable through Swagger, with a README that includes setup instructions, a tech stack summary, and a live deployment link once it's hosted.
