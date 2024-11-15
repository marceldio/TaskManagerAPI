import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

# Читаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаём синхронный движок для работы с Alembic
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем базовый класс для моделей
Base = declarative_base()
