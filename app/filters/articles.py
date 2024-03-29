from enum import Enum


class CategoryFilter(str, Enum):
    """Доступные фильтры при выборе темы статей."""
    POLITICS = 'Политика'
    ECONOMY = 'Экономика'
    SPORT = 'Спорт'
    SOCIETY = 'Общество'
    ALL = 'ВСЕ'


class SourceFilter(str, Enum):
    """Доступные фильтры при выборе источников."""
    RBC = 'РБК'
    INOSMI = 'ИноСМИ'
    ALL = 'ВСЕ'
