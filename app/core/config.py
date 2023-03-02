from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Парсинг новостей'
    app_description: str = 'API для парсинга новостных статей'

    class Config:
        env_file = '.env'


settings = Settings()
