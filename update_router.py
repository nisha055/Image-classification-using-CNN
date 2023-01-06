

from fastapi import APIRouter
from fastapi import status, HTTPException, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import schemas


action_router = APIRouter(
    prefix='/update',
    tags=['update_user']
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@action_router.put("/update/{id}", response_model=schemas.User)
def update_user(id: int, name: str, session: Session = Depends(get_session)):
    user = session.query(models.User).get(id)
    if user:
        user.name = name
        session.commit()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")
    return user


@action_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):
    user = session.query(models.User).get(id)
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")
    return None
