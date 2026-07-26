# Dashboard Stats

from fastapi import APIRouter
from sqlalchemy import func
from .application import user_dependency, db_dependency
from models import Application, Company
from starlette import status

router = APIRouter(
    prefix='/dashboard',
    tags=['dashboard']
)

# GET /dashboard/stats — count of the logged-in user's applications, grouped by status
@router.get('/stats', status_code=status.HTTP_200_OK)
async def get_stats(db: db_dependency, user: user_dependency):
    stats = db.query(Application.status, func.count(Application.id)) \
        .join(Company) \
        .filter(Company.owner_id == user.get('id')) \
        .group_by(Application.status) \
        .all()

    return {s: c for s, c in stats}