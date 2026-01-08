from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import ArticleTag, Tag, db, Article
from slugify import slugify


users_bp = Blueprint("users", __name__)

@users_bp.route("/articles")
@jwt_required()
def user_articles():
    user_id = get_jwt_identity()
    articles = Article.query.filter_by(author_id=int(user_id)).all()

    user_articles = []
    for article in articles:
        user_articles.append({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "featured_image_url": article.featured_image_url,
            "read_time_minutes": article.read_time_minutes,
            "status": article.status,
            "published_at": article.published_at,
            "content": article.content,
            "author_id": article.author_id,
        })

    return user_articles