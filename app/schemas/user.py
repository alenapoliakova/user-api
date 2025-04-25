from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, constr


class UserBase(BaseModel):
    model_config = ConfigDict(
        strict=True,  # Запрещает дополнительные поля
        str_to_lower=False,  # Запрещает автоматическое приведение к нижнему регистру
        validate_assignment=True,  # Валидация при присваивании значений
        extra='forbid'  # Запрещает дополнительные поля
    )
    name: str = Field(..., max_length=64)
    surname: str = Field(..., max_length=64)
    patronymic: str | None = Field(None, max_length=64)
    type: constr(pattern="^(teacher|student|headteacher)$")
    class_name: str | None = Field(None, max_length=8)
    login: str = Field(..., max_length=64)
    subject: str | None = Field(None, max_length=64)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        strict=True,
        str_to_lower=False,
        validate_assignment=True,
        extra='forbid'
    )
    name: str | None = Field(None, max_length=64)
    surname: str | None = Field(None, max_length=64)
    patronymic: str | None = Field(None, max_length=64)
    type: constr(pattern="^(teacher|student|headteacher)$") | None = None
    class_name: str | None = Field(None, max_length=8)
    login: str | None = Field(None, max_length=64)
    password: str | None = Field(None, min_length=8)
    subject: str | None = Field(None, max_length=64)


class UserFilter(BaseModel):
    model_config = ConfigDict(
        strict=True,
        str_to_lower=False,
        validate_assignment=True,
        extra='forbid'
    )
    name: str | None = Field(None, max_length=64)
    surname: str | None = Field(None, max_length=64)
    patronymic: str | None = Field(None, max_length=64)
    type: constr(pattern="^(teacher|student|headteacher)$") | None = None
    class_name: str | None = Field(None, max_length=8)
    login: str | None = Field(None, max_length=64)
    subject: str | None = Field(None, max_length=64)
