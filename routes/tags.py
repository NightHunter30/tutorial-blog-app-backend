from flask import request, jsonify, Blueprint
from models import db, Tag
from utils.auth import token_required

tags_bp = Blueprint("tags", __name__)
#app.py url_prefix /tags
@tags_bp.route("", methods=["POST"])
@token_required
def create_tag_route():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Tag name is required!"})
    
    tagName = data.get("name")
    existing_tag = Tag.query.filter_by(name=tagName).first()
    if existing_tag:
        return jsonify({"error": "Tag name already exists!"})

    tag = Tag(name=tagName)
    db.session.add(tag)
    db.session.commit()
    return jsonify({
        "message": "tag successfully created!",
        "tag": {
            "id": tag.id,
            "name": tag.name,
        }
    })

@tags_bp.route("", methods=["GET"])
def get_all_tags_route():
    tags = Tag.query.all()
    tags_list = []
    for tag in tags:
        tags_list.append({
            "id": tag.id,
            "name": tag.name,
        })
    return jsonify({
        "message": "Tags retrieved successfully!",
        "tags": tags_list
    })

@tags_bp.route("/<int:tag_id>", methods=["GET"])
def get_tag_by_id_route(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found!"})
    
    return jsonify({
        "message": "Tag retrieved successfully!",
        "tag": {
            "id": tag.id,
            "name": tag.name,
        }
    })

@tags_bp.route("/<int:tag_id>", methods=["PUT"])
@token_required
def update_tag_route(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found!"})
    
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Tag name is required!"})
    
    new_name = data.get("name")
    existing_tag = Tag.query.filter_by(name=new_name).first()
    if existing_tag and existing_tag.id != tag_id:
        return jsonify({"error": "Tag name already exists!"})
    
    tag.name = new_name
    db.session.commit()
    
    return jsonify({
        "message": "Tag updated successfully!",
        "tag": {
            "id": tag.id,
            "name": tag.name,
        }
    })

@tags_bp.route("/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_tag_route(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found!"})
    
    db.session.delete(tag)
    db.session.commit()
    
    return jsonify({
        "message": "Tag deleted successfully!"
    })
