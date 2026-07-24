# Register -> Login -> JWT created -> JWT used for further actions
import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv() 

SECRET_KEY =  os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Class Create User Request - Username, password +++ needed
class CreateUserRequest(BaseModel):
    username : str
    first_name : str
    last_name : str
    password : str
    email : str
    role : str


# Class for token
# Inside class we need, Authenticate User, create_Access_token, Get current user.

class Token(BaseModel):
    access_token : str
    token_type : str

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session, Depends(get_db)]
    
def authenticate_user(username : str, password : str, db):
    user = db.query(Users).filter(username == Users.username).first() # db.query(class).filter(x==y).first() 
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id : int, role : str, expires_delta = timedelta(minutes=20)): 
    encode = {'sub' : username, 'id' : user_id, 'role' :role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]): # Had to revise the Oauth2 concepts.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')

        # Verification~!

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role} #All correct~!
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')

# @Router Post : 1. Create User and 2. login for acess Token.
