from telegram import Update
from telegram.ext import (CallbackQueryHandler, CommandHandler, ContextTypes,
                          ConversationHandler)

from .jobs import (get_articles, get_or_create_user, get_user_article_limit,
                   update_user_article_limit)
from .menu import (CATEGORY_MENU_NUM, CATEGORY_MENU_TXT, MAIN_MENU_NUM,
                   MAIN_MENU_TXT, SETTINGS_MENU_NUM, SETTINGS_MENU_TXT,
                   SOURCE_MENU_NUM, SOURCE_MENU_TXT, category_keyboard,
                   main_keyboard, pattern, settings_keyboard, source_keyboard)


async def start_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Управление главным меню после команды /start."""
    chat_id = update.effective_chat.id
    await get_or_create_user(chat_id)
    await update.message.reply_text(MAIN_MENU_TXT, reply_markup=main_keyboard)
    return MAIN_MENU_NUM


async def start_over_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Повторный возврат в главное меню без создания сообщения."""
    context.user_data.clear()
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(MAIN_MENU_TXT, reply_markup=main_keyboard)
    return MAIN_MENU_NUM


async def source_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Управление меню источников."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        SOURCE_MENU_TXT, reply_markup=source_keyboard
    )
    return SOURCE_MENU_NUM


async def category_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Управление меню тем."""
    query = update.callback_query
    source = query.data
    context.user_data['source'] = source
    await query.answer()
    await query.edit_message_text(
        CATEGORY_MENU_TXT,
        reply_markup=category_keyboard
    )
    return CATEGORY_MENU_NUM


async def article_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Получение статей и возврат главного меню."""
    chat_id = update.effective_chat.id
    query = update.callback_query
    category = query.data
    source = context.user_data['source']
    # await query.answer(f'Выбрано: {source} - {category}')
    await query.delete_message()
    msg_txt = f'Статьи из {source}'
    if source == 'ВСЕ':
        msg_txt = 'Статьи из всех источников'
    if category == 'ВСЕ':
        msg_txt += ' по всем темам:'
    else:
        msg_txt += f' на тему {category}:'
    await context.bot.send_message(chat_id, msg_txt)
    articles = await get_articles(chat_id, category, source)
    # Если нет статей - сообщить об этом.
    for article in articles:
        # Получаем данные статьи: id, title, picture, overview, category
        id = article.id
        title = article.title
        picture = article.picture_link
        if not picture:
            # Временная заглушка
            picture = 'https://t-bike.ru/images/products/no-image.jpg'
        overview = article.overview
        if not overview:
            overview = ''
        article_cat = article.category
        # Отправляем InlineKeyBoard:
        # картинка (если есть, нет - заглушка), текст, кнопка читать:
        # в тексте: title, overview (если есть), category
        # в кнопке - url на нужный эндпоинт с указанием id статьи
        # TODO: template, эндпоинт для получения html-страницы
        await context.bot.send_photo(chat_id, picture, caption=title)
    await context.bot.send_message(
        chat_id,
        MAIN_MENU_TXT,
        reply_markup=main_keyboard
    )
    return MAIN_MENU_NUM


async def settings_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Управление меню настроек."""
    query = update.callback_query
    chat_id = update.effective_chat.id
    article_limit = await get_user_article_limit(chat_id)
    await query.answer()
    await query.edit_message_text(
        SETTINGS_MENU_TXT(article_limit),
        reply_markup=settings_keyboard
    )
    return SETTINGS_MENU_NUM


async def settings_update_manager(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Возврат в меню настроек после обновления изменения article_limit."""
    query = update.callback_query
    chat_id = update.effective_chat.id
    new_limit = int(query.data)
    await update_user_article_limit(chat_id, new_limit)
    return await settings_manager(update, context)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_manager)],
    states={
        MAIN_MENU_NUM: [
            CallbackQueryHandler(
                source_manager,
                pattern=pattern(SOURCE_MENU_NUM)
            ),
            CallbackQueryHandler(
                settings_manager,
                pattern=pattern(SETTINGS_MENU_NUM)
            ),
        ],
        SOURCE_MENU_NUM: [
            CallbackQueryHandler(
                start_over_manager,
                pattern=pattern(MAIN_MENU_NUM)
            ),
            CallbackQueryHandler(category_manager),
        ],
        CATEGORY_MENU_NUM: [
            CallbackQueryHandler(
                source_manager,
                pattern=pattern(SOURCE_MENU_NUM)
            ),
            CallbackQueryHandler(article_manager),
        ],
        SETTINGS_MENU_NUM: [
            CallbackQueryHandler(
                start_over_manager,
                pattern=pattern(MAIN_MENU_NUM)
            ),
            CallbackQueryHandler(settings_update_manager),
        ],
    },
    fallbacks=[CommandHandler('start', start_over_manager)],
)
