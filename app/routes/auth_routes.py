from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.models.schemas import UserCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)

    db.add(new_user)
    try:
        await db.commit()
    except:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}
