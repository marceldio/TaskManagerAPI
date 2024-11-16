from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.models import User
from app.models.schemas import UserCreate, UserLogin
from app.auth.utils import verify_password, create_access_token, authenticate_user
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.utils import authenticate_user
from app.db.database import get_db
from app.auth.utils import hash_password

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


# Аутентификация пользователя
@router.post("/register", status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)

    db.add(new_user)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}



@router.post("/login")
async def login_for_access_token(
    username: str, password: str, db: AsyncSession = Depends(get_db)
):
    db_user = await authenticate_user(username, password, db)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Логика для создания токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
