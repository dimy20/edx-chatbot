
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import init_db
from api.v1 import users, conversations, courses

init_db()

app = FastAPI()
origins = [
    "http://localhost:5173",
]

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,  # Allows cookies to be sent in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (e.g., Authorization, Content-Type)
)

app.include_router(users.router, prefix=users.PREFIX, tags=["users"])
app.include_router(conversations.router, prefix=conversations.PREFIX, tags=["conversations"])
app.include_router(courses.router, prefix=courses.PREFIX, tags=["courses"])