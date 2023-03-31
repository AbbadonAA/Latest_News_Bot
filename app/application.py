from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description
    )
    app.include_router(main_router)

    @app.on_event('startup')
    async def on_startup():
        """Действия при запуске сервера."""
        # Создание первого суперпользователя:
        await create_first_superuser()
        # Добавить запуск бота.

    @app.on_event('shutdown')
    async def on_shutdown():
        """Действия при остановке сервера."""
        # Добавить остановку бота.
        ...

    return app
