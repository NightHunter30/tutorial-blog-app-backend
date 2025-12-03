from flask import request, jsonify,Blueprint
from models import db, User
from utils.auth import hash_password, verify_password
from utils.jwt import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required!"})
    
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists!"})
    
    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "user successfully created!",
        "user_id": user.id
    })

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required!"})
    
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid credentials!"})
    
    if not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials!"})
    
    token = create_access_token(user.id)

    return jsonify({
        "message": "Login successful!",
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    })


