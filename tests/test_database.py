from sqlalchemy.orm import Session
from app.db.database import async_engine
from app.models.models import User, Task

# Проверка подключения и выполнения запросов
def test_database_operations():
    try:
        # Открываем сессию
        with Session(async_engine) as session:
            # 1. Проверяем, можно ли получить записи из таблиц
            print("=== Fetching data from the database ===")
            users = session.query(User).all()
            tasks = session.query(Task).all()
            print(f"Users: {users}")
            print(f"Tasks: {tasks}")

            # 2. Добавляем нового пользователя
            print("=== Adding a new user ===")
            new_user = User(username="testuser", password_hash="hashed_password")
            session.add(new_user)
            session.commit()
            print(f"Added user: {new_user}")

            # 3. Добавляем новую задачу для этого пользователя
            print("=== Adding a new task ===")
            new_task = Task(
                title="Test Task",
                description="This is a test task.",
                status="in_progress",
                user_id=new_user.id
            )
            session.add(new_task)
            session.commit()
            print(f"Added task: {new_task}")

            # 4. Проверяем связанные данные
            print("=== Fetching tasks for the new user ===")
            user_with_tasks = session.query(User).filter_by(id=new_user.id).first()
            print(f"User: {user_with_tasks.username}, Tasks: {user_with_tasks.tasks}")

    except Exception as e:
        print(f"Error: {e}")

# Запуск проверки
if __name__ == "__main__":
    test_database_operations()
