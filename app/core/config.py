from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Парсинг'
    app_description: str = 'API для запуска парсеров'

    class Config:
        env_file = '.env'


settings = Settings()
