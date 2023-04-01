# import logging
from .handlers import start_handler
from telegram.ext import Application, ApplicationBuilder, CommandHandler

from app.core.config import settings

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


def create_bot() -> Application:
    """Создание бота."""
    bot_instance = ApplicationBuilder().token(settings.bot_token).build()
    bot_instance.add_handler(CommandHandler('start', start_handler))
    return bot_instance


async def start_bot() -> Application:
    """Запуск бота."""
    bot_instance = create_bot()
    await bot_instance.initialize()
    await bot_instance.updater.start_polling()
    await bot_instance.start()
    return bot_instance
