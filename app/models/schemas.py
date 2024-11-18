from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Схема для создания нового пользователя
class UserLogin(BaseModel):
    username: str
    password: str


# Схема для создания токена доступа
class Token(BaseModel):
    access_token: str
    token_type: str


# Схема для статуса задачи (в процессе, завершено)
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

    model_config = ConfigDict(from_attributes=True)


# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.in_progress

    model_config = ConfigDict(from_attributes=True)


# Схема для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

    model_config = ConfigDict(from_attributes=True)


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str


# Схема для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
