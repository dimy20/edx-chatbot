from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import Course
from db.db import get_db
from edx.edx import EdxClient, clean_overview
from dotenv import load_dotenv
import os
from chat.chat import gen_overview_embeddings
from pydantic import BaseModel

router = APIRouter()
PREFIX="/api/v1/courses"
load_dotenv()
edx = EdxClient(host="http://local.openedx.io:8000", access_token=os.getenv("OPENEDX_API_ACCESS_TOKEN"))
#por ahora agregar un curso solo tiene en cuenta el course overview

class CourseCreate(BaseModel):
    name: str
    user_id: str

# anadir login dependecy para este endpoint, por ahora user id es cualquiera
@router.post("/")
async def add_course(course: CourseCreate, db: Session = Depends(get_db)):
    #Is this course in edx?
    course_data = edx.find_course_by_name(course.name)

    if not course_data:
        raise HTTPException(status_code=404, detail=f"The course {course.name} doesnt exist")

    course_db = Course(name=course.name, user_id=course.user_id)
    db.add(course_db)
    db.commit()
    db.refresh(course_db)

    overview = clean_overview(course_data["overview"])
    embeddings_ids = gen_overview_embeddings(overview_text=overview, course_id=course_db.id)

    return {
        "course" : course.name,
        "status" : "Success",
        "embeddings_ids": embeddings_ids
    }