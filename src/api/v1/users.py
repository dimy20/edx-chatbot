from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import models
from db.db import get_db

from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()
PREFIX="/api/v1/users"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    courses: Optional[List[str]] = [] 
    conversations: Optional[List[str]] = []

    class Config:
        orm_mode = True

@router.post("/")
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(email=user.email, name = user.name, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "status" : "Success",
            "user_added: " : db_user.as_dict()
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )

@router.get("/{name}")
async def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
