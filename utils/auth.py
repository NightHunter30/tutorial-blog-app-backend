from functools import wraps
from flask import request, jsonify
from utils.jwt import verify_token
import bcrypt

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed_password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def token_required(f):
    """Authentication decorator that requires a valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Authorization: Bearer WQWEQWEQWEQWEQWEQWE
        # [Bearer, WQWEQWEQWEQWEQWEQWE]

        # Check if token is in header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Verify token
        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Add user info to request
        request.user_id = payload.get('sub')

        return f(*args, **kwargs)
    return decorated
