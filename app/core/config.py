import uuid
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Настройки проекта."""
    # Настройки приложения:
    APP_TITLE: str = 'LATEST NEWS PARSER'
    APP_DESCRIPTION: str = (
        'API для запуска парсеров и получения новостных статей')
    HOST: str
    PORT: int
    DOMAIN: bool
    DOMAIN_NAME: str
    DEBUG: bool = False
    # Настройки БД:
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    # Хеширование токенов:
    SECRET: str = str(uuid.uuid4())
    # Бизнес-логика:
    PARSER_FREQUENCY: int
    STORAGE_DAYS: int
    # Первый суперпользователь:
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    FIRST_SUPERUSER_CHAT_ID: Optional[int] = None
    # Данные бота:
    IP: str = '127.0.0.1'
    WEBHOOK: bool
    BOT_TOKEN: str
    BOT_PERSISTENCE_FILE: str = str(
        BASE_DIR / 'app' / 'bot' / 'data' / 'bot_persistence_file')
    # Настройки логгирования:
    LOG_LOCATION: str = 'logs/warning.log'
    LOG_ROTATION: str = '12:00'
    LOG_COMPRESSION: str = 'tar.gz'
    LOG_LEVEL: str = 'WARNING'

    @property
    def database_url(self) -> str:
        """Получение ссылки для подключения к БД."""
        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'
        )

    @property
    def telegram_webhook_url(self) -> str:
        """Получить ссылку на эндпоинт для работы бота в режиме webhook."""
        return urljoin(self.DOMAIN_NAME, "telegram/webhook")

    class Config:
        env_file = '.env'


settings = Settings()
