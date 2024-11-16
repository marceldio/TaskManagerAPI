from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.schemas import TaskCreate, TaskOut
from app.models.models import Task
from typing import List

router = APIRouter()

# POST-запрос для создания задачи
@router.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate):
    with SessionLocal() as db:  # Используем SessionLocal для работы с базой
        new_task = Task(**task.dict(), user_id=1)  # Установлен тестовый user_id
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

# GET-запрос для получения всех задач
@router.get("/", response_model=List[TaskOut])
def get_tasks():
    with SessionLocal() as db:  # Используем SessionLocal для работы с базой
        tasks = db.query(Task).all()
        return tasks
