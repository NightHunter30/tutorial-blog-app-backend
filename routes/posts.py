from flask import request, jsonify, Blueprint
from models import db, User, Tag, Post
from utils.auth import token_required

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("", methods=["POST"])
@token_required
def create_post_route():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    user_id = request.user_id
    tag_ids = data.get("tag_ids")
    if not title or not content:
        return jsonify({"error": "Title and content are required!"})
    if not tag_ids or len(tag_ids) < 0:
        return jsonify({"error": "Please select tags"})
    
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(post)
    db.session.commit()

    tags_dicts = []
    for tag in tags:
        tags_dicts.append({
            "id": tag.id,
            "name": tag.name
        })

    return ({
        "message": "post created successfully!",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            # "tags": [{"id": tag.id, "name": tag.name} for tag in tags]
            "tags": tags_dicts
        } 
    })

#/posts
@posts_bp.route("", methods=["GET"])
def get_all_posts_route():
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        tags_dicts = []
        for tag in post.tags:
            tags_dicts.append({
                "id": tag.id,
                "name": tag.name
            })
        posts_list.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "tags": tags_dicts
        })
    
    return jsonify({
        "message": "Posts retrieved successfully!",
        "posts": posts_list
    })

@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post_by_id_route(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"})
    
    tags_dicts = []
    for tag in post.tags:
        tags_dicts.append({
            "id": tag.id,
            "name": tag.name
        })
    
    return jsonify({
        "message": "Post retrieved successfully!",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "tags": tags_dicts
        }
    })

@posts_bp.route("/<int:post_id>", methods=["PUT"])
@token_required
def update_post_route(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"})
    
    if post.user_id != request.user_id:
        return jsonify({"error": "Go away, this post can only be edited by its creators!"}), 403
    
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    tag_ids = data.get("tag_ids")
    
    
    if not title or not content:
        return jsonify({"error": "Title and content are required!"})
    
    post.title = title
    post.content = content
    
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags = tags
    
    db.session.commit()
    
    tags_dicts = []
    for tag in post.tags:
        tags_dicts.append({
            "id": tag.id,
            "name": tag.name
        })
    
    return jsonify({
        "message": "Post updated successfully!",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "tags": tags_dicts
        }
    })

@posts_bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post_route(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"})
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({
        "message": "Post deleted successfully!"
    })