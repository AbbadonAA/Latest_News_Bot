from enum import Enum


class ThemeFilter(str, Enum):
    """Доступные фильтры при выборе темы статей."""
    POLITICS = 'Политика'
    ECONOMY = 'Экономика'
    SPORT = 'Спорт'
    SOCIETY = 'Общество'
