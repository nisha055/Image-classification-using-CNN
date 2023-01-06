
from fastapi import APIRouter
from fastapi import status, HTTPException, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import schemas


add_router = APIRouter(
    prefix='/add',
    tags=['add_user']
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@add_router.post("/user", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    userdb = models.User(name=user.name)
    session.add(userdb)
    session.commit()
    session.refresh(userdb)
    return userdb


@add_router.post("/username")
def post_username(name: str, session: Session = Depends(get_session)):
    userdb = models.User(name=name)
    session.add(userdb)
    session.commit()
    session.refresh(userdb)
    return name
