from typing import Optional

from fastapi_users import schemas
from pydantic import validator


class UserRead(schemas.BaseUser[int]):
    """Схема - получение данных пользователя."""
    chat_id: Optional[int]
    article_limit: int


class UserCreate(schemas.BaseUserCreate):
    """Схема - создание пользователя."""
    chat_id: Optional[int]
    article_limit: int = 5

    @validator('article_limit')
    def validate_article_limit(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Количество статей: от 1 до 10.')
        return v


class UserUpdate(schemas.BaseUserUpdate):
    """Схема - изменение пользователя."""
    chat_id: Optional[int]
    article_limit: Optional[int]

    @validator('article_limit', pre=True, always=True)
    def validate_article_limit(cls, v):
        if v is None:
            return v
        if v < 1 or v > 10:
            raise ValueError('Количество статей: от 1 до 10.')
        return v
