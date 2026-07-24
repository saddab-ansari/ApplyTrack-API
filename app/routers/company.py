# Company CRUD
# A Pydantic CompanyRequest model for the request body (name, location)
# GET /companies — all companies belonging to the logged-in user
# POST /companies — create one, tied to user.get('id')
# PUT / DELETE /companies/{id} — same ownership-check pattern as the Todo app's update_todo/delete_todo

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Company
from starlette import status

router = APIRouter(
    prefix='/company',
    tags=['company']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Here, we don't assign any 'id' to the company,
# Assigning an existing id crashes the create_company() function 
# And most importantly - If we don't assign it then the SQLAlchemy itself generates an ID
# Helps keep the User experience easier and keep the app safe as well in a very simple way~!

class CompanyRequest(BaseModel):
    name: str
    location: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_company(user: user_dependency, db: db_dependency):
    return db.query(Company).filter(Company.owner_id == user.get('id')).all()

# Create a Company:

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(user: user_dependency, db: db_dependency, company_request: CompanyRequest):
    company_model = Company(**company_request.model_dump(), owner_id=user.get('id'))
    db.add(company_model)
    db.commit()


@router.put("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_company(user: user_dependency, db: db_dependency,
                         company_update: CompanyRequest, company_id: int = Path(gt=0)):
    
    company_model = db.query(Company).filter(Company.id == company_id) \
        .filter(Company.owner_id == user.get('id')).first()

    if company_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    
    company_model.name = company_update.name
    company_model.location = company_update.location

    db.add(company_model)
    db.commit()


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(user: user_dependency, db: db_dependency, company_id: int = Path(gt=0)):

    company_model = db.query(Company).filter(company_id == Company.id) \
        .filter(user.get('id') == Company.owner_id).first()
    if company_model is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.query(Company).filter(Company.id == company_id).filter(Company.owner_id == user.get('id')).delete()
    db.commit()
