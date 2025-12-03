from jose import jwt
from datetime import datetime, timedelta
from flask import current_app

def create_access_token(user_id):
    expire = datetime.utcnow() + timedelta(minutes=30)
    data = {
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(user_id),
    }
    token = jwt.encode(data, current_app.config["JWT_SECRET_KEY"], "HS256")
    return token

# verify function in here
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return decoded_token
    except:
        return None