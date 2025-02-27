import secrets
import uuid
from flask import request, make_response
from functools import wraps

from app.configuration import logging, TOKEN_COOKIE_NAME

def generate_token():
    return str(uuid.uuid4())

def get_or_create_user_token(response=None):
    token = request.cookies.get(TOKEN_COOKIE_NAME)
    
    if not token:
        token = generate_token()
        logging.info(f"Generated new user token: {token}")
        
        if response:
            response.set_cookie(TOKEN_COOKIE_NAME, token, max_age=31536000)
    
    return token

def with_user_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        get_or_create_user_token(response)
        return response
    return decorated_function
