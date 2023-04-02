from telegram import Update
from telegram.ext import ContextTypes

from .jobs import get_or_create_user


async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    chat_id = update.effective_chat.id
    user = await get_or_create_user(chat_id)
    text = f'Вы зарегистрированы. Chat_id: {user.chat_id}'
    await context.bot.send_message(chat_id=chat_id, text=text)
