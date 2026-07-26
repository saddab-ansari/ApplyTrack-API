# ApplyTrack API

**Stack:** FastAPI · SQLAlchemy · SQLite · JWT Auth · python-dotenv


A backend API for tracking my own job application pipeline — companies, roles, and interview rounds, built from scratch without a course. Full scope, constraints, and feature breakdown: [`problem_statement.md`](./problem_statement.md)

## 🔗 Links to the deployed project.

**🧠 Backend only link** : https://applytrack-api-3tpm.onrender.com <br>
*This link takes you to the fastapi swagger UI where you can test all the endpoints!*<br>

**🧠 Full stack link** : https://apply-track-api.vercel.app <br>
*This link utilizes AI-generated frontend, so that you can experience my work, without fighting with swagger UI. The Backend is untouched.*<br>

## Data model

<img width="1432" height="885" alt="Flowchart" src="https://github.com/user-attachments/assets/f1fe8938-f387-4344-88ed-1c2726b9eeac" />

## Current status — where I'm at right now

- [x] Auth (register, login, JWT) + `.env` config
- [x] Company CRUD
- [x] Application CRUD + status transitions
- [x] Interview rounds (nested under applications)
- [x] Filtering, sorting, pagination
- [x] Dashboard stats endpoint

*Status: Completed and Deployed*

## Setup

```bash
git clone <repo-url>
cd applytrack-api
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
