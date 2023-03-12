from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Настройки проекта."""
    app_title: str = 'LATEST NEWS PARSER'
    app_description: str = (
        'API для запуска парсеров и получения новостных статей')
    # настройки БД:
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

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
