
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, Text, Table, Column, Integer, ForeignKey
from datetime import datetime

db = SQLAlchemy()

# posts_tags
# post_id 1
# tag_id 1

posts_tags = Table(
    "posts_tags",
    db.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str]  = mapped_column(String(255), nullable=False)
    # This column to have roles in our app such as user,admin,manager, etc
    role: Mapped[str]  = mapped_column(String(255), nullable=False, default="user")
    posts = db.relationship("Post", back_populates="user")
    created_at: Mapped[datetime]  = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime]  = mapped_column(server_default=func.now(), onupdate=func.now())

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    content: Mapped[str]  = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    # post.user and will also have user.posts
    user = db.relationship("User", back_populates="posts")
    # define many to many relationship between post and tags
    tags = db.relationship("Tag", secondary=posts_tags, back_populates="posts")
    created_at: Mapped[datetime]  = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime]  = mapped_column(server_default=func.now(), onupdate=func.now())

class Tag(db.Model):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime]  = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime]  = mapped_column(server_default=func.now(), onupdate=func.now())

    posts = db.relationship("Post", secondary=posts_tags, back_populates="tags")