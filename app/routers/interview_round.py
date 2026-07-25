# InterviewRound CRUD
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models import InterviewRound, Application, Company
from sqlalchemy.orm import Session
from database import SessionLocal
from .auth import get_current_user
from pydantic import BaseModel
from starlette import status

# A Pydantic InterviewRoundRequest model for the request body (stage, date, result)
#   — no application_id in the body; it comes from the URL path instead.
#   — no id, same reasoning as Company/Application.

router = APIRouter(
    tags=['rounds']
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[Session, Depends(get_current_user)]

class InterviewRoundRequest(BaseModel):
    stage : str
    date : datetime
    result : str

# POST /application/{application_id}/rounds — create a round under a specific application

@router.post('/application/{application_id}/rounds', status_code=status.HTTP_201_CREATED)
async def create_round(db: db_dependancy, user: user_dependancy,
                       application_id: int, create_round_request: InterviewRoundRequest):

    application = db.query(Application).join(Company)\
        .filter(Application.id == application_id)\
        .filter(Company.owner_id == user.get('id')).first()

    if application is None:
        raise HTTPException(status_code=401, detail='User not authorized')

    round_model = InterviewRound(**create_round_request.model_dump(), application_id=application_id)
    db.add(round_model)
    db.commit()

# GET /application/{application_id}/rounds

@router.get('/application/{application_id}/rounds', status_code=status.HTTP_200_OK)
async def get_all_rounds(db : db_dependancy, user : user_dependancy, application_id : int):
    rounds_model = db.query(InterviewRound).join(Application).join(Company)\
        .filter(InterviewRound.application_id == application_id)\
        .filter(Company.id == Application.company_id)\
        .filter(Company.owner_id == user.get('id')).all()

    if not rounds_model:
        raise HTTPException(status_code=401, detail='User not authorized')
    return rounds_model

# GET /rounds/{id}

@router.get('/rounds/{id}', status_code=status.HTTP_200_OK)
async def get_round_by_id(db : db_dependancy, user : user_dependancy, id : int):

    rounds_model = db.query(InterviewRound).join(Application).join(Company)\
        .filter(InterviewRound.id == id)\
        .filter(Application.id == InterviewRound.application_id)\
        .filter(Company.id == Application.company_id)\
        .filter(Company.owner_id == user.get('id')).first()

    if rounds_model is None:
        raise HTTPException(status_code=401, detail='User not authorized')
    return rounds_model
    
# PUT /rounds/{id}

@router.put('/rounds/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_round(db : db_dependancy, user : user_dependancy, \
                       id : int, update_request : InterviewRoundRequest):

    rounds_model = db.query(InterviewRound).join(Application).join(Company)\
        .filter(InterviewRound.id == id)\
        .filter(Application.id == InterviewRound.application_id)\
        .filter(Company.id == Application.company_id)\
        .filter(Company.owner_id == user.get('id')).first()

    if rounds_model is None:
        raise HTTPException(status_code=401, detail='User not authorized')

    rounds_model.stage = update_request.stage
    rounds_model.date = update_request.date
    rounds_model.result = update_request.result

    db.add(rounds_model)
    db.commit()

# DELETE /rounds/{id}

@router.delete('/rounds/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_round(db : db_dependancy, user : user_dependancy, id : int):

    rounds_model = db.query(InterviewRound).join(Application).join(Company)\
        .filter(InterviewRound.id == id)\
        .filter(Application.id == InterviewRound.application_id)\
        .filter(Company.id == Application.company_id)\
        .filter(Company.owner_id == user.get('id')).first()   

    if rounds_model is None:
        raise HTTPException(status_code=401, detail='User not authorized')

    db.query(InterviewRound).filter(InterviewRound.id == id).delete()
    db.commit()

