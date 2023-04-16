from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    """Настройки проекта."""
    # настройки приложения:
    APP_TITLE: str = 'LATEST NEWS PARSER'
    APP_DESCRIPTION: str = (
        'API для запуска парсеров и получения новостных статей')
    HOST: str
    PORT: int
    DOMAIN: bool
    DOMAIN_NAME: str
    # настройки БД:
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    # хеширование токенов:
    SECRET: str = 'SECRET'
    # бизнес-логика:
    DAYS: int
    # первый суперпользователь:
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    FIRST_SUPERUSER_CHAT_ID: Optional[int] = None
    # данные бота:
    BOT_TOKEN: str

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
