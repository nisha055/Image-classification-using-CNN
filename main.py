from typing import List
from fastapi import FastAPI, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from fastapi.middleware.cors import CORSMiddleware
import add_router
import update_router
import text_model_router
import img_model_router


Base.metadata.create_all(engine)

description = """
Sample FastApi App covering following things : 

## Users

You will be able to:

* **Create users**
* **View users List**
* **View users by ID**
* **Update users**
* **Delete users**


"""

tags_metadata = [
    {
        "name": "text_model",
        "description": "Operations with text inputs.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "img_model",
        "description": "Operations with img inputs.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "view_user",
        "description": "Operations with users.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "add_user",
        "description": "Operations with users.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "update_user",
        "description": "Operations with users.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="SampleFastAPI App",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Nisha Priya",
        "email": "abc@deloitte.com",
    },
    license_info={
        "name": "Abc license",
        "url": "https://abc.com",
    },
    openapi_tags=tags_metadata
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "Users"


@app.get("/user/{id}", response_model=schemas.User, tags=["view_user"])
def read_user_path(id: int, session: Session = Depends(get_session)):
    user = session.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")
    return user


@app.get("/username")
def read_user_query(id: int, session: Session = Depends(get_session), tags=["view_user"]):
    user = session.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")
    return user


@app.get("/user", response_model=List[schemas.User], tags=["view_user"])
def get_user_list(session: Session = Depends(get_session)):
    user_list = session.query(models.User).all()
    return user_list


@app.get("/user-json")
def get_user_list_json(session: Session = Depends(get_session)):
    user_list = session.query(models.User).all()
    return user_list


app.include_router(add_router.add_router)
app.include_router(update_router.action_router)
app.include_router(text_model_router.text_model_router)
app.include_router(img_model_router.img_model_router)
