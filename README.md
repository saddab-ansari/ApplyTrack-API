# ApplyTrack API

**Stack:** FastAPI · SQLAlchemy · SQLite · JWT Auth · python-dotenv

A backend API for tracking my own job application pipeline — companies, roles, and interview rounds, built from scratch without a course. Full scope, constraints, and feature breakdown: [`problem_statement.md`](./problem_statement.md)

## Data model

<img width="1432" height="885" alt="Flowchart" src="https://github.com/user-attachments/assets/f1fe8938-f387-4344-88ed-1c2726b9eeac" />

## Current status — where I'm at right now

- [x] Auth (register, login, JWT) + `.env` config
- [x] Company CRUD
- [ ] Application CRUD + status transitions
- [ ] Interview rounds (nested under applications)
- [ ] Filtering, sorting, pagination
- [ ] Dashboard stats endpoint

*Added Database, Models, Authentication (with JWT) And Company CRUD Moving towards application router*

## Setup

```bash
git clone <repo-url>
cd applytrack-api
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
