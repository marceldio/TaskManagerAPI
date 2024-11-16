from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Асинхронный движок
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Функция получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
