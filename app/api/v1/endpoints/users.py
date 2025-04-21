import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


async def get_user_by_login(db: AsyncSession, login: str) -> User | None:
    """Получить пользователя по login."""
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()


async def check_login_availability(db: AsyncSession, login: str) -> None:
    """Проверить доступность login."""
    if await get_user_by_login(db, login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists"
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
    await check_login_availability(db, user.login)

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


@router.get("/{login}", response_model=UserResponse)
async def get_user(
    login: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по login."""
    user = await get_user_by_login(db, login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{login}", response_model=UserResponse)
async def update_user(
    login: str,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Полностью обновить данные пользователя."""
    existing_user = await get_user_by_login(db, login)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.login != login:
        await check_login_availability(db, user.login)

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


@router.patch("/{login}", response_model=UserResponse)
async def update_user_partial(
    login: str,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Частично обновить данные пользователя."""
    existing_user = await get_user_by_login(db, login)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user.dict(exclude_unset=True)

    if "login" in update_data and update_data["login"] != login:
        await check_login_availability(db, update_data["login"])

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


@router.delete("/{login}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    login: str,
    db: AsyncSession = Depends(get_db)
):
    """Удалить пользователя."""
    user = await get_user_by_login(db, login)
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
