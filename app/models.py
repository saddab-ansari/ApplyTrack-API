from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

# User → Company → Application → InterviewRound

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, index=True, primary_key=True, unique=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    location = Column(String)

class Application(Base):
    __tablename__ = 'application'

    id= Column(Integer, index=True, primary_key=True, unique=True)
    company_id = Column(Integer,ForeignKey('company.id'))
    job_role = Column(String)
    salary = Column(Integer)
    status = Column(String, default="applied")

class Interview_Round(Base):
    __tablename__ = 'interview_round'

    id = Column(Integer, index=True, primary_key=True, unique=True)
    application_id = Column( Integer, ForeignKey('application.id'))
    stage = Column(String) 
    date = Column(DateTime)
    result = Column(String) # Because either its positive or negative but can also be pending   
