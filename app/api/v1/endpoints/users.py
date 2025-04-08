from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Get user info",
    operation_id="get_user_by_id",
    responses={
        status.HTTP_200_OK: {
            "description": "User found"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found"
        }
    }
)
async def get_user_by_id(
        id: str,
        db: AsyncSession = Depends(get_db)
):
    # Check if user with this id exists
    result = await db.execute(
        select(User).where(User.id == id)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    # Return user
    try:
        return existing_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error when finding a user: {str(e)}"
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    operation_id="delete_user",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found"
        }
    }
)
async def delete_user(
        id: str,
        db: AsyncSession = Depends(get_db)
):
    # Check if user with this id exists
    result = await db.execute(
        select(User).where(User.id == id)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user
    try:
        await db.delete(existing_user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error when deleting a user: {str(e)}"
        )

@router.patch("/{email}", response_model=UserResponse)
async def update_user_partial(
    email: str
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Check if user with same email exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exists"
        )

    for field, value in user.dict(exclude_unset=True, exclude={"email", "password"}).items():
        setattr(user, field, value)

    if user.email:
        # Check if user with same email exists
        result = await db.execute(
            select(User).where(User.email == user.email)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with new email already exists"
            )
        existing_user.email = user.email

    if user.password:
        # Hash the password
        password_hash = bcrypt.hashpw(
            user.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        existing_user.password_hash = password_hash
    
    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)
    
    return existing_user


@router.put("/{email}", response_model=UserResponse)
async def update_user(
    email: str
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if user with same email exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exists"
        )

    for field, value in user.dict(exclude_unset=True, exclude={"email", "password"}).items():
        setattr(user, field, value)

    # Check if user with same email exists
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with new email already exists"
        )
    existing_user.email = user.email

    # Hash the password
    password_hash = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    existing_user.password_hash = password_hash
    
    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)
    
    return existing_user
