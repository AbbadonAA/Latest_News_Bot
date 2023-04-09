# Вариант подстрочного меню на основе ReplyKeyboardMarkup

import telegram
from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from app.filters.articles import SourceFilter, ThemeFilter

from .jobs import (get_or_create_user, get_user_article_limit,
                   update_user_article_limit)

CON_TYPE = ContextTypes.DEFAULT_TYPE

MAIN_MENU, SOURCE_MENU, THEME_MENU, SETTINGS_MENU = range(4)

MAIN_KEYBOARD = [['Статьи', 'Настройки']]
SOURCE_KEYBOARD = [[s.value for s in SourceFilter], ['Назад']]
THEME_KEYBOARD = [[t.value for t in ThemeFilter], ['Назад']]
SETTINGS_KEYBOARD = [[str(lt) for lt in range(1, 11)], ['Назад']]


async def reply_with_keyboard(
    update: Update,
    text: str,
    keyboard: list[list[str]],
    menu: int
):
    """Шаблон ответа с выбором клавиатуры и меню."""
    await update.message.reply_text(
        text=text,
        reply_markup=telegram.ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True
        )
    )
    return menu


async def get_main_menu(update: Update):
    """Вызов главного меню."""
    text = 'Нажмите "Статьи" для получения последних новостей:'
    keyboard = MAIN_KEYBOARD
    menu = MAIN_MENU
    return await reply_with_keyboard(update, text, keyboard, menu)


async def get_settings_menu(update: Update):
    """Вызов меню настроек."""
    chat_id = update.effective_chat.id
    article_limit = await get_user_article_limit(chat_id)
    text = (
        'Выберите количество получаемых статей.\n'
        f'Сейчас выбрано: {article_limit}')
    keyboard = SETTINGS_KEYBOARD
    menu = SETTINGS_MENU
    return await reply_with_keyboard(update, text, keyboard, menu)


async def get_source_menu(update: Update):
    """Вызов меню источников."""
    text = 'Выберите источник:'
    keyboard = SOURCE_KEYBOARD
    menu = SOURCE_MENU
    return await reply_with_keyboard(update, text, keyboard, menu)


async def get_theme_menu(update: Update):
    """Вызов меню тем."""
    text = 'Выберите тему:'
    keyboard = THEME_KEYBOARD
    menu = THEME_MENU
    return await reply_with_keyboard(update, text, keyboard, menu)


async def start(update: Update, context: CON_TYPE):
    """Обработка команды /start."""
    chat_id = update.effective_chat.id
    await get_or_create_user(chat_id)
    return await get_main_menu(update)


async def manage_main_menu(update: Update, context: CON_TYPE):
    """Управление главным меню."""
    user_choice = update.message.text
    if user_choice == 'Статьи':
        return await get_source_menu(update)
    elif user_choice == 'Настройки':
        return await get_settings_menu(update)


async def manage_source_menu(update: Update, context: CON_TYPE):
    """Управление меню источников."""
    user_choice = update.message.text
    if user_choice == 'Назад':
        return await get_main_menu(update)
    context.user_data['source'] = user_choice
    return await get_theme_menu(update)


async def manage_theme_menu(update: Update, context: CON_TYPE):
    """Управление меню тем."""
    user_choice = update.message.text
    if user_choice == 'Назад':
        return await get_source_menu(update)
    context.user_data['theme'] = user_choice
    source = context.user_data['source']
    theme = context.user_data['theme']
    text = f'Источник: {source}, Тема: {theme}'
    await context.bot.send_message(update.effective_chat.id, text)
    return await get_main_menu(update)


async def manage_settings_menu(update: Update, context: CON_TYPE):
    """Управление меню настроек."""
    user_choice = update.message.text
    chat_id = update.effective_chat.id
    if user_choice == 'Назад':
        return await get_main_menu(update)
    await update_user_article_limit(chat_id, int(user_choice))
    return await get_settings_menu(update)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MAIN_MENU: [
            MessageHandler(filters.Text(MAIN_KEYBOARD[0]), manage_main_menu),
        ],
        SOURCE_MENU: [
            MessageHandler(
                filters.Text(SOURCE_KEYBOARD[0] + SOURCE_KEYBOARD[1]),
                manage_source_menu
            ),
        ],
        THEME_MENU: [
            MessageHandler(
                filters.Text(THEME_KEYBOARD[0] + THEME_KEYBOARD[1]),
                manage_theme_menu
            ),
        ],
        SETTINGS_MENU: [
            MessageHandler(
                filters.Text(SETTINGS_KEYBOARD[0] + SETTINGS_KEYBOARD[1]),
                manage_settings_menu
            ),
        ],
    },
    fallbacks=[CommandHandler('fallback', get_main_menu)],
)
