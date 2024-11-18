from fastapi import FastAPI

from app.routes import auth_routes, tasks

app = FastAPI()

# Подключение маршрутов для задач
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
