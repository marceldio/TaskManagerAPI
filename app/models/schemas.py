from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    in_progress = "in_progress"
    completed = "completed"


# Схема для отображения задачи
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: Optional[int]  # Позволяет быть None, если пользователь не установлен

    class Config:
        orm_mode = True
        from_attributes = True


# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.in_progress

    class Config:
        orm_mode = True
        from_attributes = True


# Схема для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

    class Config:
        orm_mode = True
        from_attributes = True


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str


# Схема для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
