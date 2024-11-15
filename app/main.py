from fastapi import FastAPI
from app.routes import task_routes
from app.routes import auth_routes

app = FastAPI()

# Подключение маршрутов для задач
app.include_router(task_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
