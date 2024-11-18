from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.models.models import Task
from app.models.schemas import TaskCreate, TaskOut, TaskUpdate

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


# PUT-запрос для обновления задачи
@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)
):
    # Найти задачу по ID
    result = await db.execute(select(Task).where(Task.id.__eq__(task_id)))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Обновить поля задачи
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    try:
        await db.commit()
        await db.refresh(task)
        return task
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error updating task")


# DELETE-запрос для удаления задачи
@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    # Найти задачу по ID
    result = await db.execute(select(Task).where(Task.id.__eq__(task_id)))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        await db.delete(task)
        await db.commit()
        return {"detail": "Task deleted successfully"}
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting task")
