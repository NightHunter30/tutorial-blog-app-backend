from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import ArticleTag, Tag, db, Article
from slugify import slugify


articles_bp = Blueprint("articles", __name__)

# /articles [GET] - Public endpoint to fetch all articles
@articles_bp.route("", methods=["GET"])
def get_articles():
    status = request.args.get("status", "published", type=str)
    
    query = Article.query
    
    # Filter by status if specified
    if status:
        query = query.filter_by(status=status)
    
    # Get all results ordered by published date
    all_articles = query.order_by(Article.published_at.desc()).all()
    
    articles = []
    for article in all_articles:
        article_tags = []
        for article_tag in article.article_tags:
            article_tags.append({
                "id": article_tag.tag.id,
                "title": article_tag.tag.title,
                "slug": article_tag.tag.slug,
            })
        
        articles.append({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "featured_image_url": article.featured_image_url,
            "read_time_minutes": article.read_time_minutes,
            "status": article.status,
            "author": {
                "id": article.author.id,
                "name": article.author.name,
                "email": article.author.email,
                "avatar": article.author.avatar,
            },
            "published_at": article.published_at,
            "tags": article_tags
        })
    
    return jsonify(articles)


# /articles [POST]
@articles_bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    data = request.get_json()
    author_id = get_jwt_identity()

    article = Article(
        title=data["title"],
        slug=data["slug"],
        excerpt=data["excerpt"],
        featured_image_url=data["featuredImageUrl"],
        read_time_minutes=data["readTimeMinutes"],
        status=data["status"],
        content=data["content"],
        author_id=int(author_id),
        published_at=None
    )

    db.session.add(article)
    db.session.flush()

    # ['Javascript', 'React', 'Python']
    tags = data.get("tags")
    for tag_name in tags:
        tag = Tag.query.filter_by(title=tag_name).first()
        if not tag:
            tag = Tag(title=tag_name, slug=slugify(tag_name))
            db.session.add(tag)
            db.session.flush()

        article_tag = ArticleTag(
            article_id = article.id,
            tag_id = tag.id
        )
        db.session.add(article_tag)

    db.session.commit()
    
    return jsonify({
        "message": "Article successfully created!",
        "article": {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "featured_image_url": article.featured_image_url,
            "read_time_minutes": article.read_time_minutes,
            "status": article.status,
            "content": article.content,
            "author_id": article.author_id,
            "published_at": article.published_at,
        }
    })



@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article_route(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if not article:
        return jsonify({"error": "Article not found"}), 404
    
    article_tags = []
    for article_tag in article.article_tags:
        article_tags.append({
            "id": article_tag.tag.id,
            "title": article_tag.tag.title,
            "slug": article_tag.tag.slug,
        })
    
    return jsonify({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "featured_image_url": article.featured_image_url,
            "read_time_minutes": article.read_time_minutes,
            "status": article.status,
            "content": article.content,
            "author": {
                "id": article.author.id,
                "name": article.author.name,
                "email": article.author.email,
                "avatar": article.author.avatar,
            },
            "published_at": article.published_at,
            "tags": article_tags
    })


# /articles/<id> [PUT]
@articles_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def edit_article(article_id):
    author_id = get_jwt_identity()
    article = Article.query.filter_by(id=article_id).first()
    
    if not article:
        return jsonify({"error": "Article not found"}), 404
    
    if article.author_id != int(author_id):
        return jsonify({"error": "Unauthorized: You can only edit your own articles"}), 403
    
    data = request.get_json()
    
    # Update article fields if provided
    if "title" in data:
        article.title = data["title"]
    if "slug" in data:
        article.slug = data["slug"]
    if "excerpt" in data:
        article.excerpt = data["excerpt"]
    if "featuredImageUrl" in data:
        article.featured_image_url = data["featuredImageUrl"]
    if "readTimeMinutes" in data:
        article.read_time_minutes = data["readTimeMinutes"]
    if "status" in data:
        article.status = data["status"]
    if "content" in data:
        article.content = data["content"]
    
    # Handle tags update if provided
    if "tags" in data:
        # Remove all existing article tags
        ArticleTag.query.filter_by(article_id=article.id).delete()
        
        # Add new tags
        tags = data.get("tags")
        for tag_name in tags:
            tag = Tag.query.filter_by(title=tag_name).first()
            if not tag:
                tag = Tag(title=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
                db.session.flush()
            
            article_tag = ArticleTag(
                article_id=article.id,
                tag_id=tag.id
            )
            db.session.add(article_tag)
    
    db.session.commit()
    
    # Fetch updated tags to return
    article_tags = []
    for article_tag in article.article_tags:
        article_tags.append({
            "id": article_tag.tag.id,
            "title": article_tag.tag.title,
            "slug": article_tag.tag.slug,
        })
    
    return jsonify({
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "featured_image_url": article.featured_image_url,
            "read_time_minutes": article.read_time_minutes,
            "status": article.status,
            "content": article.content,
            "author_id": article.author_id,
            "published_at": article.published_at,
            "tags": article_tags
    })