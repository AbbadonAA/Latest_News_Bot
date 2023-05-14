from loguru import logger
from telegram.ext import Application, ApplicationBuilder, PicklePersistence

from app.core.config import settings

from .handlers import conv_handler


def create_bot() -> Application:
    """Создание бота."""
    bot_persistance = PicklePersistence(settings.BOT_PERSISTENCE_FILE)
    bot_instance = (
        ApplicationBuilder()
        .token(settings.BOT_TOKEN)
        .persistence(persistence=bot_persistance)
        .build()
    )
    logger.info('Создан бот Телеграм.')
    return bot_instance


def setup_conv_handlers(bot_instance: Application) -> None:
    """Инициализация обработчиков при запуске бота."""
    bot_instance.add_handler(conv_handler)


async def start_bot(webhook_mode: bool = settings.WEBHOOK) -> Application:
    """Запуск бота."""
    bot_instance = create_bot()
    setup_conv_handlers(bot_instance)
    await bot_instance.initialize()
    if webhook_mode:
        bot_instance.updater = None
        await bot_instance.bot.set_webhook(
            url=settings.telegram_webhook_url,
            secret_token=settings.SECRET
        )
    else:
        await bot_instance.updater.start_polling()
    await bot_instance.start()
    logger.info('Запущен бот Телеграм.')
    return bot_instance
