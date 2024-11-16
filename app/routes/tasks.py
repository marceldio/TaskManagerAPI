from fastapi import APIRouter, HTTPException
from app.db.database import SessionLocal
from app.models.models import Task
from app.models.schemas import TaskCreate, TaskOut

router = APIRouter()

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate):
    new_task = Task(**task.model_dump())
    with SessionLocal() as db:  # Используем синхронную сессию
        db.add(new_task)
        try:
            db.commit()
            db.refresh(new_task)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error creating task")
    return new_task

@router.get("/", response_model=list[TaskOut])
def get_tasks():
    with SessionLocal() as db:  # Используем синхронную сессию
        tasks = db.query(Task).all()
    return tasks
