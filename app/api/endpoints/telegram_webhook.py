from fastapi import APIRouter, Request
from telegram import Update

from app.core.config import settings

router = APIRouter()

if settings.WEBHOOK:

    @router.post(
        '/webhook',
        summary='Получить обновления Telegram',
        response_description='Обновления получены',
    )
    async def get_telegram_bot_updates(request: Request) -> dict:
        """Получение обновлений Telegram в режиме webhook."""
        secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if secret_token != settings.SECRET:
            raise
        bot_instance = request.app.state.bot_instance
        request_json_data = await request.json()
        await bot_instance.update_queue.put(
            Update.de_json(data=request_json_data, bot=bot_instance.bot)
        )
        return request_json_data
