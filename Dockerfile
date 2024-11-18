FROM python:3.12-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry
RUN pip install poetry && poetry config virtualenvs.create false

# Устанавливаем зависимости из локального кэша
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app
