
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

from api.v1 import users, conversations, courses

import os


init_db()
app = FastAPI()

@app.get("/")
async def index():
    return {
        "first" : "Hello, World"
    }

app.include_router(users.router, prefix=users.PREFIX, tags=["users"])
app.include_router(conversations.router, prefix=conversations.PREFIX, tags=["conversations"])
app.include_router(courses.router, prefix=courses.PREFIX, tags=["courses"])