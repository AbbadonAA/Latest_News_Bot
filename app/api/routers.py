from fastapi import APIRouter

from app.api.endpoints import article_router, db_router

main_router = APIRouter()
main_router.include_router(
    db_router,
    prefix='/db_interact',
    tags=['Управление БД: парсинг и удаление устаревших данных']
)
main_router.include_router(
    article_router,
    prefix='/articles',
    tags=['Получение статей']
)
