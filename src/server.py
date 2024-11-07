
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from uuid import uuid4
from edx.edx import EdxClient, clean_overview
from chat.chat import gen_overview_embeddings
from db.db import init_db, SessionLocal
from db import models

from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional

import os

load_dotenv()
edx = EdxClient(host="http://local.openedx.io:8000", access_token=os.getenv("OPENEDX_API_ACCESS_TOKEN"))
init_db()
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    return {
        "first" : "Hello, World"
    }

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    courses: Optional[List[str]] = []  # List of course IDs
    conversations: Optional[List[str]] = []  # List of conversation IDs

    class Config:
        orm_mode = True

# FastAPI endpoint to add a new user
@app.post("/user/add")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name = user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/user/{name}")
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#por ahora agregar un curso solo tiene en cuenta el course overview
@app.post("/course/add/{course_name}")
async def add_course(course_name: str):
    course_data = edx.find_course_by_name(course_name)
    if not course_data:
        raise HTTPException(status_code=404, detail=f"The course {course_name} doesnt exist")

    overview = clean_overview(course_data["overview"])
    course_id = course_data["id"]

    embeddings_ids = gen_overview_embeddings(overview_text=overview, course_id=course_id)

    return {
            "course" : course_name,
            "status" : "Success",
            "embeddings_ids": embeddings_ids
    }

