from flask import Flask, request, jsonify
from models import db
from routes.posts import posts_bp
from routes.tags import tags_bp
from routes.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_blog_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "1b8797c955940205fccea47d3cd47abf"

# Pass the app object to db object of flask-sqlalchemy
db.init_app(app)

app.register_blueprint(posts_bp, url_prefix="/posts")
app.register_blueprint(tags_bp, url_prefix="/tags")
app.register_blueprint(auth_bp, url_prefix="/auth")

# Creates the database tables
with app.app_context():
    db.create_all()