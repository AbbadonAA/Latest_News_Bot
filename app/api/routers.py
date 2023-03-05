from fastapi import APIRouter

from app.api.endpoints import news_router, parser_router

main_router = APIRouter()
main_router.include_router(
    parser_router,
    prefix='/parse_news',
    tags=['Парсинг новостей']
)
main_router.include_router(
    news_router,
    prefix='/news_router',
    tags=['Получение статей']
)
