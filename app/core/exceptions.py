from http import HTTPStatus


class ApplicationError:
    """Исключение для бизнес-логики приложения."""
    detail: str = "Неопознанная ошибка. Будет исправлена."


class UnauthorizedError(ApplicationError):
    status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED
    detail = "У Вас нет прав для просмотра запрошенной страницы."
