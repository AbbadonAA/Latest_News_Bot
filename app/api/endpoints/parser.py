from fastapi import APIRouter

router = APIRouter()


@router.get('/parser')
async def parse_news():
    ans = {
        'title': 'Заголовок статьи',
        'image': 'Картинка',
        'description': 'Краткое описание',
        'text': 'Текст статьи',
        'link': 'Ссылка на статью',
        'authors': 'Авторы'
    }
    return ans
