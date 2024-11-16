from app.models.schemas import TaskCreate, TaskOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.models.models import Task

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    # Асинхронное выполнение запроса
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = Task(**task.model_dump(), user_id=1)
    db.add(new_task)
    try:
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error creating task")
