from fastapi import APIRouter

from app.api.endpoints import parser_router

main_router = APIRouter()
main_router.include_router(
    parser_router,
    prefix='/parse_news',
    tags=['News Parser']
)
