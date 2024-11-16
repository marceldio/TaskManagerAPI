from app.models.schemas import TaskCreate, TaskOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import Task

router = APIRouter()


@router.get("/")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    # Пример: получение данных
    tasks = await db.execute("SELECT * FROM tasks")
    return tasks.fetchall()


@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate):
    new_task = Task(**task.model_dump())
    with get_db() as db:  # Используем синхронную сессию
        db.add(new_task)
        try:
            db.commit()
            db.refresh(new_task)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error creating task")
    return new_task
