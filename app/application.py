from fastapi import FastAPI

from app.api.routers import main_router
from app.bot.main import start_bot
from app.core.config import settings
from app.core.init_db import create_first_superuser


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION
    )
    app.include_router(main_router)

    @app.on_event('startup')
    async def on_startup():
        """Действия при запуске сервера."""
        # Создание первого суперпользователя:
        await create_first_superuser()
        bot_instance = await start_bot()
        app.state.bot_instance = bot_instance

    @app.on_event('shutdown')
    async def on_shutdown():
        """Действия при остановке сервера."""
        bot_instance = app.state.bot_instance
        await bot_instance.updater.stop()
        # Для webhook:
        # await bot_instance.stop()
        # await bot_instance.shutdown()

    return app
