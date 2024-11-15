from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import os
from dotenv import load_dotenv
from app.db.database import Base
# Убедитесь, что эти импорты не удаляются сборщиком, так как они регистрируют модели в Base.metadata
from app.models.models import User, Task

# Загружаем переменные окружения
load_dotenv()

# Настройка Alembic
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Настройка логгера
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные для моделей
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в 'офлайн' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в 'онлайн' режиме."""
    connectable = create_engine(  # Используем синхронный движок
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    print(f"Using database URL: {os.getenv('DATABASE_URL')}")
    run_migrations_offline()
else:
    print(f"Database URL: {os.getenv('DATABASE_URL')}")
    run_migrations_online()
