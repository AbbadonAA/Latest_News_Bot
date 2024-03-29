from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from app.core.db import Base


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    """Модель для пользователей."""
    chat_id = mapped_column(Integer, nullable=True, index=True, unique=True)
    article_limit = mapped_column(Integer, nullable=False, default=5)
