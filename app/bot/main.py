# import logging
from telegram.ext import Application, ApplicationBuilder

from app.core.config import settings

from .handlers import conv_handler

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


def create_bot() -> Application:
    """Создание бота."""
    bot_instance = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    bot_instance.add_handler(conv_handler)
    return bot_instance


async def start_bot() -> Application:
    """Запуск бота."""
    bot_instance = create_bot()
    await bot_instance.initialize()
    await bot_instance.updater.start_polling()
    await bot_instance.start()
    return bot_instance