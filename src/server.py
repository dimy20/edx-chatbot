
from fastapi import FastAPI, UploadFile
from fastapi import HTTPException
from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4

from edx.edx import EdxClient, clean_overview
from chat.chat import gen_overview_embeddings

import os
load_dotenv()

edx = EdxClient(host="http://local.openedx.io:8000", access_token=os.getenv("OPENEDX_API_ACCESS_TOKEN"))

UPLOAD_DIRECTORY = Path("uploaded-pdfs")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

app = FastAPI()
@app.get("/")
async def index():
    return {
        "first" : "Hello, World"
    }

#por ahora agregar un curso solo tiene en cuenta el course overview
@app.post("/course/add/{course_name}")
async def add_course(course_name: str):
    course_data = edx.find_course_by_name(course_name)
    if not course_data:
        raise HTTPException(status_code=404, detail=f"The course {course_name} doesnt exist")

    overview = clean_overview(course_data["overview"])
    embeddings_ids = gen_overview_embeddings(overview_text=overview)

    return {
            "status" : "Success",
            "embeddings_ids": embeddings_ids
    }

