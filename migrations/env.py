import asyncio
import os

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.database import Base

# Настройка Alembic
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
target_metadata = Base.metadata


def do_run_migrations(connection):
    """Синхронный метод для запуска миграций."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'онлайн' режиме (асинхронно)."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)  # Передаем синхронную функцию
    await connectable.dispose()


def run_migrations_offline() -> None:
    """Запуск миграций в 'офлайн' режиме."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
