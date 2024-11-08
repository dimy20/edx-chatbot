
from fastapi import FastAPI
from db.db import init_db
from api.v1 import users, conversations, courses

init_db()
app = FastAPI()
app.include_router(users.router, prefix=users.PREFIX, tags=["users"])
app.include_router(conversations.router, prefix=conversations.PREFIX, tags=["conversations"])
app.include_router(courses.router, prefix=courses.PREFIX, tags=["courses"])