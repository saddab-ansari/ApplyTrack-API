# Main.py will be used in the end to route all the files.

from fastapi import FastAPI
import models
from database import engine
from routers import auth,company,application, interview_round, dashboard
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(application.router)
app.include_router(interview_round.router)
app.include_router(dashboard.router)
