from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    """Настройки проекта."""
    # настройки приложения:
    app_title: str = 'LATEST NEWS PARSER'
    app_description: str = (
        'API для запуска парсеров и получения новостных статей')
    HOST: str
    PORT: int
    DOMAIN: str
    # настройки БД:
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    # хеширование токенов:
    secret: str = 'SECRET'
    # бизнес-логика:
    DAYS: int
    # первый суперпользователь:
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    first_superuser_chat_id: Optional[int] = None
    # данные бота:
    bot_token: str

    @property
    def database_url(self) -> str:
        """Получение ссылки для подключения к БД."""
        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'
        )

    class Config:
        env_file = '.env'


settings = Settings()
