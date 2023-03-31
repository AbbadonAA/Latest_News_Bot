from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserModel


async def get_all_users_from_db(
    session: AsyncSession,
) -> list[UserModel]:
    """Получение списка пользователей."""
    stmt = select(UserModel)
    users = await session.execute(stmt)
    return users.scalars().all()
