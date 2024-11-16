from fastapi import APIRouter, HTTPException
from app.db.database import SessionLocal
from app.models.models import User
from app.models.schemas import UserCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=201)
def register_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)

    with SessionLocal() as db:  # Используем синхронную сессию
        db.add(new_user)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}
