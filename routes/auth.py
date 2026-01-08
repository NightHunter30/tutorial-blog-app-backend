from flask import request, jsonify,Blueprint
from models import db, User
from utils.auth import hash_password, verify_password
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required!"})
    
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists!"})
    
    user = User(email=email, password_hash=hash_password(password), name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User successfully created!",
        "user": {
            "id": user.id,
            "email": user.email
        }
    })

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required!"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid credentials!"}), 401

    if not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials!"}), 401

    access = create_access_token(identity=str(user.id))
    refresh = create_refresh_token(identity=str(user.id))

    response = jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    })
    set_access_cookies(response, access)
    set_refresh_cookies(response, refresh)

    return response

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    response = jsonify({"msg": "refreshed"})
    set_access_cookies(response, access)
    return response

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat() if user.created_at else None
    })

@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # Update allowed fields
    if "name" in data:
        user.name = data["name"]
    if "avatar" in data:
        user.avatar = data["avatar"]

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    })