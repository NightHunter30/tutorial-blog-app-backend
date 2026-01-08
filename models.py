
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, Text, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str]  = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(500), nullable=True)
    # This column to have roles in our app such as user,admin,manager, etc
    role: Mapped[str]  = mapped_column(String(255), nullable=False, default="user")
    created_at: Mapped[datetime]  = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime]  = mapped_column(server_default=func.now(), onupdate=func.now())

    # Relationship
    articles = relationship("Article", back_populates="author")

class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    featured_image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    read_time_minutes: Mapped[str] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship
    author = relationship("User", back_populates="articles")
    article_tags = relationship("ArticleTag", back_populates="article")

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Point tag back to article tag
    article_tags = relationship("ArticleTag", back_populates="tag")


class ArticleTag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"), nullable=False)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("tag_id", "article_id", name="uq_article_tag"),
    )

    # Relationships
    article = relationship("Article", back_populates="article_tags")
    tag = relationship("Tag", back_populates="article_tags")
