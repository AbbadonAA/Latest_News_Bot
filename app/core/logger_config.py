import sys

from loguru import logger

from .config import settings


def setup_logging():
    """Настройка логгирования."""
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        settings.LOG_LOCATION,
        rotation=settings.LOG_ROTATION,
        compression=settings.LOG_COMPRESSION,
        level=settings.LOG_LEVEL,
    )
