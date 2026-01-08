from datetime import timedelta
from flask import Flask, request, jsonify
from models import db
from routes.auth import auth_bp
from routes.articles import articles_bp
from routes.user import users_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_blog_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "1b8797c955940205fccea47d3cd47abf"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=4, minutes=30)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# Initialize JWT Manager
jwt = JWTManager(app)

# Pass the app object to db object of flask-sqlalchemy
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(articles_bp, url_prefix="/articles")
app.register_blueprint(users_bp, url_prefix="/users")

# Creates the database tables
with app.app_context():
    db.create_all()