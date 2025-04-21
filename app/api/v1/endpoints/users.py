from typing import List

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserFilter, UserResponse, UserUpdate

router = APIRouter()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Получить пользователя по email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def check_email_availability(db: AsyncSession, email: str) -> None:
    """Проверить доступность email."""
    if await get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )


def hash_password(password: str) -> str:
    """Хешировать пароль."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать нового пользователя."""
    await check_email_availability(db, user.email)

    user_data = user.dict(exclude={"password"})
    user_data["password_hash"] = hash_password(user.password)

    new_user = User(**user_data)
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/{email}", response_model=UserResponse)
async def get_user(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по email."""
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{email}", response_model=UserResponse)
async def update_user(
    email: str,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Полностью обновить данные пользователя."""
    existing_user = await get_user_by_email(db, email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.email != email:
        await check_email_availability(db, user.email)

    for field, value in user.dict(exclude={"password"}).items():
        setattr(existing_user, field, value)

    existing_user.password_hash = hash_password(user.password)

    try:
        await db.commit()
        await db.refresh(existing_user)
        return existing_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.patch("/{email}", response_model=UserResponse)
async def update_user_partial(
    email: str,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Частично обновить данные пользователя."""
    existing_user = await get_user_by_email(db, email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user.dict(exclude_unset=True)

    if "email" in update_data and update_data["email"] != email:
        await check_email_availability(db, update_data["email"])

    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(existing_user, field, value)

    try:
        await db.commit()
        await db.refresh(existing_user)
        return existing_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Удалить пользователя."""
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )


@router.get("/user_filter", response_model=List[UserResponse])
async def get_users(
    user_filter: UserFilter,
    db: AsyncSession = Depends(get_db)
):
    filter_data = filter.dict(exclude_unset=True)
    filters = [key == value for key, value in filter_data]
    result = await db.execute(select(User).filter(and_(*filters)))
    users = result.scalars().all()
    return users
