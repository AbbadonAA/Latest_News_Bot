from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from app.core.db import Base

from .user import UserModel


class ArticleUser(Base):
    """Модель для связи статей и прочитавших их пользователей."""
    article_id = Column(
        Integer,
        ForeignKey('article.id', ondelete='CASCADE'),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    )


class Infographic(Base):
    """Модель для инфографики к статье."""
    article_id: Mapped[int] = mapped_column(
        ForeignKey('article.id', ondelete='CASCADE'))
    infographic_link: Mapped[str] = mapped_column(String)
    articles: Mapped[list['Article']] = (
        relationship('Article', back_populates='infographic_links'))


class Author(Base):
    """Модель для автора статьи."""
    article_id: Mapped[int] = mapped_column(
        ForeignKey('article.id', ondelete='CASCADE'))
    author_name: Mapped[str] = mapped_column(String)
    articles: Mapped[list['Article']] = (
        relationship('Article', back_populates='authors'))


class Article(Base):
    """Модель для статьи."""
    date = mapped_column(type_=TIMESTAMP(timezone=True), nullable=False)
    category = mapped_column(String, nullable=False)
    title = mapped_column(String, nullable=False)
    overview = mapped_column(Text, nullable=True)
    text = mapped_column(Text, nullable=True)
    link = mapped_column(String, nullable=False, unique=True)
    picture_link = mapped_column(String, nullable=True)
    video_link = mapped_column(String, nullable=True)
    video_preview_link = mapped_column(String, nullable=True)
    infographic_links: Mapped[list['Infographic']] = (
        relationship(
            'Infographic',
            back_populates='articles',
            lazy='selectin',
            cascade='all, delete-orphan'
        )
    )
    authors: Mapped[list['Author']] = (
        relationship(
            'Author',
            back_populates='articles',
            lazy='selectin',
            cascade='all, delete-orphan'
        )
    )
    readers: Mapped[list['UserModel']] = (
        relationship(
            'UserModel',
            secondary='articleuser'
        )
    )
    source = mapped_column(String, nullable=False)
