# Application CRUD

from typing import Annotated
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Application, Company
from .company import user_dependency
from starlette import status

router = APIRouter(
    prefix='/application',
    tags=['application']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class ApplicationRequest(BaseModel):
    company_id : int
    job_role : str
    salary : int

# No Status here - User might enter wrong status or forget to fill it in entirely - and lose all the data of its status.
# No id required - SQLAlchemy does it automatically (faster and safer)

class StatusUpdateRequest(BaseModel):
    status: str

# Response schemas — needed so FastAPI actually serializes the nested `rounds`
# relationship instead of silently dropping it (SQLAlchemy relationships are
# lazy-loaded; without an explicit schema asking for `.rounds`, it never gets touched).

class InterviewRoundResponse(BaseModel):
    id: int
    stage: str
    date: datetime
    result: str

    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    id: int
    company_id: int
    job_role: str
    salary: int
    status: str
    rounds: list[InterviewRoundResponse] = []

    class Config:
        from_attributes = True

# GET /application/ 

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_application(
    db: db_dependency,
    user: user_dependency,
    application_status: str = None,
    sort_by: str = "id",
    skip: int = 0,
    limit: int = 10):

    application_model = db.query(Application).join(Company) \
        .filter(Application.company_id == Company.id) \
        .filter(Company.owner_id == user.get('id'))

    if application_status is not None:
        application_model = application_model.filter(Application.status == application_status)

    if sort_by is not None:
        if sort_by == "salary":
            application_model = application_model.order_by(Application.salary)
        elif sort_by == "id":
            application_model = application_model.order_by(Application.id)
        elif sort_by in ["job_role", "job role"]:
            application_model = application_model.order_by(Application.job_role)

    application_model = application_model.offset(skip).limit(limit).all()

    if not application_model:
        raise HTTPException(status_code=404, detail='Application not found')
    
    return application_model

# GET /application/{id}      
# single application, same ownership check

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ApplicationResponse)
async def get_application(db: db_dependency, user: user_dependency, id: int):
    application_model = db.query(Application).join(Company) \
        .filter(Application.id == id) \
        .filter(Company.owner_id == user.get('id')).first()
    if application_model is None:
        raise HTTPException(status_code=404, detail='Application not found')
    return application_model

# POST /application/   
# BEFORE creating: Worked on User authentication, to avoid users modifying others applications. 

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_application(db: db_dependency, user: user_dependency, application_request: ApplicationRequest):
    company = db.query(Company).filter(Company.id == application_request.company_id).first()
    if company is None or company.owner_id != user.get('id'):
        raise HTTPException(status_code=401, detail='User not authorized')

    application_model = Application(**application_request.model_dump())
    db.add(application_model)
    db.commit()


# PUT /application/{id}      
# update job_role, salary, company_id (NOT status)

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_application(db : db_dependency, user : user_dependency, id : int, update_request : ApplicationRequest):

    application_model = db.query(Application).join(Company) \
        .filter(Application.id == id).filter(Company.owner_id == user.get('id')).first()

    if application_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    application_model.id = id
    application_model.company_id = update_request.company_id
    application_model.job_role = update_request.job_role
    application_model.salary = update_request.salary

    db.add(application_model)
    db.commit()
    
# PATCH /application/{id}/status

@router.patch('/{id}/status', status_code=status.HTTP_204_NO_CONTENT)
async def update_status(db : db_dependency, user : user_dependency, id : int, status_update_request : StatusUpdateRequest):
    application_model = db.query(Application).join(Company).filter(Application.id == id) \
        .filter(Company.owner_id == user.get('id')).first()
    if application_model is None:
       raise HTTPException(status_code=404, detail='Item not found')
    application_model.status = status_update_request.status
    db.add(application_model)
    db.commit()

# DELETE /application/{id}

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(db : db_dependency, user : user_dependency, id : int):
    application_model = db.query(Application).join(Company).filter(Application.id == id)\
        .filter(Company.owner_id == user.get('id')).first()
    if application_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.query(Application).filter(Application.id == id).delete()
    db.commit()
