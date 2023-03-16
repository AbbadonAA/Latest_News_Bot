from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator


class Author(BaseModel):
    author_name: str

    class Config:
        orm_mode = True


class Infographic(BaseModel):
    infographic_link: str

    class Config:
        orm_mode = True


class Article(BaseModel):
    id: int
    source: str
    date: datetime
    category: str
    title: str
    overview: Optional[str]
    text: Optional[str]
    link: str
    picture_link: Optional[str]
    video_link: Optional[str]
    authors: list[Author] = []
    infographic_links: list[Infographic] = []

    @validator('date')
    def change_date_format(cls, value):
        # Pydantic не учитывает timezone, хотя в БД всё корректно.
        # Пока такой простой костыль исправляет это поведение.
        value = value + timedelta(hours=3)
        return value.strftime('%d/%m/%Y %H:%M')

    class Config:
        orm_mode = True
