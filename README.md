# ApplyTrack API

**Stack:** FastAPI · SQLAlchemy · SQLite · JWT Auth · python-dotenv

A backend API I built from scratch, without a course, to track my own job application pipeline — every company I've applied to, every role under each company, and every interview round tied to a given application, from OA through offer or rejection.

It started as a stress-test: I'd just finished a JWT-authenticated Todo API as a guided course project, and wanted to see how much of that actually stuck once there was no instructor's code to lean on. It grew into a fully working, deployed, four-table relational API with real ownership scoping, filtering, and a nested interview-round relationship. Full design rationale and constraints: [`problem_statement.md`](./problem_statement.md).

## 🔗 Try it live

**Backend only** → https://applytrack-api-3tpm.onrender.com/docs
Takes you straight to the FastAPI Swagger UI, where every endpoint is testable directly.

**Full stack** → https://apply-track-api.vercel.app
A minimal frontend (AI-generated, so I could put my own time into the backend) wrapping the same API — the backend itself is identical between the two links.

> *Both run on free tiers, so the first request after a while idle can take ~30–60 seconds to wake the server up. Everything after that is instant.*

## What it does

- **Auth** — register, log in, get a JWT. Secrets live in `.env`, never in source.
- **Companies** — track every company you're applying to, fully scoped to your own account.
- **Applications** — one or more roles per company, each with its own status (`wishlist` → `applied` → `oa` → `interviewing` → `offer` / `rejected` / `withdrawn`).
- **Interview rounds** — attach as many rounds as you want to a single application (OA, Technical, HR...), each with its own date and outcome — returned nested inside the application automatically via a SQLAlchemy `relationship()`.
- **Filtering, sorting, pagination** — narrow applications down by status, sort by salary or role, page through results.
- **Dashboard stats** — one endpoint, one query, application counts grouped by status.

Every route above is ownership-scoped — a logged-in user can only ever see or modify their own companies, applications, and rounds, enforced at the query level, not just the UI.

## Swagger UI 
<img width="973" height="824" alt="ApplyTrack Swagger" src="https://github.com/user-attachments/assets/5d75b84a-b723-457d-9e75-e94065fd6f37" />

## Frontend UI

<img width="1315" height="717" alt="UI1" src="https://github.com/user-attachments/assets/37c739b0-b9a0-414d-ad9c-6c127238dfc1" />

<img width="1322" height="880" alt="U2" src="https://github.com/user-attachments/assets/6ceb6521-c746-4037-a456-208db4137852" />

## Data model

<img width="1432" height="885" alt="Flowchart" src="https://github.com/user-attachments/assets/f1fe8938-f387-4344-88ed-1c2726b9eeac" />

`User → Company → Application → InterviewRound` — every level below `User` carries its own foreign key back up the chain, and every read/write query joins through that chain to confirm ownership before touching a row.

## Setup (Windows)

These steps assume Python 3.10+ is already installed. Any terminal works — Command Prompt, PowerShell, or Git Bash — with one PowerShell-specific note below.

**1. Get the code**

With Git:
```
git clone https://github.com/saddab-ansari/ApplyTrack-API.git
cd ApplyTrack-API
```

Without Git: click the green **Code** button on the GitHub repo page → **Download ZIP** → extract it → open a terminal inside the extracted folder.

**2. Create and activate a virtual environment**

```
python -m venv venv
```

If Windows doesn't recognize `python`, try `py -m venv venv` instead.

Activate it:
- **Command Prompt:** `venv\Scripts\activate`
- **PowerShell:** `venv\Scripts\Activate.ps1`

> If PowerShell blocks this with a "running scripts is disabled" error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then try activating again.

You'll know it worked when you see `(venv)` at the start of your terminal prompt.

**3. Move into the backend folder and install dependencies**

The backend code lives inside the `app/` folder:

```
cd app
pip install -r requirements.txt
```

**4. Set up your `.env` file**

Still inside `app/`, copy the example file:

```
copy .env.example .env
```

Open `.env` and fill in your own `SECRET_KEY` and `ALGORITHM` (see `.env.example` for the exact format — `ALGORITHM=HS256` works as-is; generate your own `SECRET_KEY` rather than reusing a shared example).

**5. Run the server**

```
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser — that's the Swagger UI, where every endpoint can be tested directly.

### Testing the frontend against your local backend (optional)

`frontend/index.html` has `API_BASE` pointed at the live Render deployment by default, so the hosted Vercel link works instantly for anyone with no setup. To point it at your local server instead, open `frontend/index.html`, find the `API_BASE` line near the top of the `<script>` tag, and temporarily set it to:

```js
const API_BASE = "http://127.0.0.1:8000";
```

Then open the file directly in your browser. Don't commit that change — the version in the repo should stay pointed at production so the live demo keeps working for everyone else.

## Status

All core features complete and deployed. Stretch goals (Alembic migrations, a small `pytest` suite, an admin role endpoint) are documented but not yet built — see [`problem_statement.md`](./problem_statement.md) for the full breakdown.
