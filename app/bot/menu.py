from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.config import settings
from app.filters.articles import CategoryFilter, SourceFilter

# Номера меню для ConversationHandler:
MAIN_MENU_NUM, SOURCE_MENU_NUM, CATEGORY_MENU_NUM, SETTINGS_MENU_NUM = range(4)
# Текст в меню:
MAIN_MENU_TXT = 'Выберите действие:'
SOURCE_MENU_TXT = 'Выберите источник из доступных:'
CATEGORY_MENU_TXT = 'Выберите тему из доступных:'
SETTINGS_MENU_TXT = 'Выбрано статей для получения: <b>{}</b>'.format


def keyboard_constructor(
    buttons: dict[str, str],
    n_cols: int = 5,
    back_button: str = None,
    url: str = None
):
    """Конструктор клавиатур для различных меню."""
    keyboard = []
    for i in range(0, len(buttons), n_cols):
        keyboard.append(
            [
                InlineKeyboardButton(btn, callback_data=clb, url=url)
                for btn, clb in list(buttons.items())[i: i + n_cols]
            ]
        )
    if back_button:
        back_button = [
            InlineKeyboardButton('Назад', callback_data=back_button)
        ]
        keyboard.append(back_button)
    return InlineKeyboardMarkup(keyboard)


def article_keyboard(article_id: int, domain: bool = settings.DOMAIN):
    """Клавиатура для сообщения с новостной статьей."""
    url = f'http://{settings.HOST}:{settings.PORT}/articles/html/{article_id}'
    if domain:
        url = f'{settings.DOMAIN_NAME}/articles/html/{article_id}'
    keyboard = keyboard_constructor({'Читать далее': None}, url=url)
    return keyboard


def pattern(menu):
    return '^' + str(menu) + '$'


main_keyboard = keyboard_constructor(
    {'Статьи': str(SOURCE_MENU_NUM), 'Настройки': str(SETTINGS_MENU_NUM)}
)
source_keyboard = keyboard_constructor(
    {s.value: s.value for s in SourceFilter},
    back_button=str(MAIN_MENU_NUM)
)
category_keyboard = keyboard_constructor(
    {c.value: c.value for c in CategoryFilter},
    back_button=str(SOURCE_MENU_NUM)
)
settings_keyboard = keyboard_constructor(
    {str(s): str(s) for s in range(1, 11)},
    back_button=str(MAIN_MENU_NUM)
)
