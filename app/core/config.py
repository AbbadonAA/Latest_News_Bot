from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'LATEST NEWS PARSER'
    app_description: str = (
        'API для запуска парсеров и получения новостных статей')
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
