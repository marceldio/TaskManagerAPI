from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import TaskCreate, TaskOut
from app.db.database import get_db
from app.models.models import Task
from typing import List
from sqlalchemy.future import select  # Импорт select из SQLAlchemy
from app.models.models import Task as TaskModel  # Импорт TaskModel



router = APIRouter()

@router.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = Task(**task.dict(), user_id=1)  # Установил тестовый user_id

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskOut])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel))
    tasks = result.scalars().all()
    return tasks  # Возвращаем объекты TaskModel


