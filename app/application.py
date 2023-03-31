from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description
    )
    app.include_router(main_router)

    @app.on_event('startup')
    async def on_startup():
        """Запуск бота при старте сервера."""
        ...

    @app.on_event('shutdown')
    async def on_shutdown():
        """Остановка бота при остановке сервера."""
        ...

    return app
