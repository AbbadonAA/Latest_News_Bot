from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема - получение данных пользователя."""
    chat_id: int


class UserCreate(schemas.BaseUserCreate):
    """Схема - создание пользователя."""
    chat_id: int


class UserUpdate(schemas.BaseUserUpdate):
    """Схема - изменение пользователя."""
    chat_id: Optional[int]
