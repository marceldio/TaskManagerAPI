from fastapi import APIRouter
from app.models.schemas import TaskCreate, TaskOut
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.models import Task

router = APIRouter()

# POST-запрос для создания задачи
@router.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate):
    with get_db() as db:
        new_task = Task(**task.dict(), user_id=1)  # Установлен тестовый user_id
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

# GET-запрос для получения всех задач
@router.get("/")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    with get_db() as db:
        tasks = db.query(Task).all()
        return tasks
