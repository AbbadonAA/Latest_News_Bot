from fastapi import APIRouter

router = APIRouter()


@router.get('/get_news')
async def get_news():
    """Получение выбранного количества новых статей."""
    ans = {
        'title': 'Заголовок статьи',
        'image': 'Картинка',
        'description': 'Краткое описание',
        'text': 'Текст статьи',
        'link': 'Ссылка на статью',
        'authors': 'Авторы'
    }
    return ans
