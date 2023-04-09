from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.filters.articles import SourceFilter, ThemeFilter

# Номера меню для ConversationHandler:
MAIN_MENU_NUM, SOURCE_MENU_NUM, THEME_MENU_NUM, SETTINGS_MENU_NUM = range(4)
# Текст в меню:
MAIN_MENU_TXT = 'Выберите действие:'
SOURCE_MENU_TXT = 'Выберите источник из доступных:'
THEME_MENU_TXT = 'Выберите тему из доступных:'
SETTINGS_MENU_TXT = 'Выбрано статей для получения: {}'.format


def keyboard_constructor(
    buttons: dict[str, str],
    n_cols: int = 5,
    back_button: str = None
):
    """Конструктор клавиатур для различных меню."""
    keyboard = []
    for i in range(0, len(buttons), n_cols):
        keyboard.append(
            [
                InlineKeyboardButton(btn, callback_data=clb)
                for btn, clb in list(buttons.items())[i: i + n_cols]
            ]
        )
    if back_button:
        back_button = [
            InlineKeyboardButton('Назад', callback_data=back_button)
        ]
        keyboard.append(back_button)
    return InlineKeyboardMarkup(keyboard)


def pattern(menu):
    return '^' + str(menu) + '$'


main_keyboard = keyboard_constructor(
    {'Статьи': str(SOURCE_MENU_NUM), 'Настройки': str(SETTINGS_MENU_NUM)}
)
source_keyboard = keyboard_constructor(
    {s.value: s.value for s in SourceFilter},
    back_button=str(MAIN_MENU_NUM)
)
theme_keyboard = keyboard_constructor(
    {t.value: t.value for t in ThemeFilter},
    back_button=str(SOURCE_MENU_NUM)
)
settings_keyboard = keyboard_constructor(
    {str(s): str(s) for s in range(1, 11)},
    back_button=str(MAIN_MENU_NUM)
)
