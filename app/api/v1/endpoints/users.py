from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from app.db.base import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if user with same email exists
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    # Hash the password
    password_hash = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Create new user
    db_user = User(
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        password_hash=password_hash,
        type=user.type,
        class_name=user.class_name,
        email=user.email
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user
