from fastapi import APIRouter

router = APIRouter()


@router.get('/site_1')
async def site_1():
    ans = {
        'title': 'Заголовок статьи',
        'image': 'Картинка',
        'description': 'Краткое описание',
        'text': 'Текст статьи',
        'link': 'Ссылка на статью',
        'authors': 'Авторы'
    }
    return ans


@router.get('/site_2')
async def site_2():
    ans = {
        'title': 'Заголовок статьи',
        'image': 'Картинка',
        'description': 'Краткое описание',
        'text': 'Текст статьи',
        'link': 'Ссылка на статью',
        'authors': 'Авторы'
    }
    return ans
