from fastapi import FastAPI
from app.routes import task_routes

app = FastAPI()

# Подключение маршрутов для задач
app.include_router(task_routes.router, prefix="/api")
