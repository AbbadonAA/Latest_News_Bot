from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    authors: list[Author] = []
    infographic_links: list[Infographic] = []

    class Config:
        orm_mode = True
