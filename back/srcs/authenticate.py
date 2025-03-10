from flask import request, abort
from .security import Security
from .models import User

class Authenticate:
    def authenticate(request, need_enabled=False):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, description="No token provided")
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

        try:
            username, user_id = Security.decode_jwt(token)
        except Exception as e:
            abort(401, description="Invalid token")

        user_model = User()
        user = user_model.select(username=username)
        if not user or user[0].id != user_id:
            user = user_model.select(id=user_id)
            if not user:
                abort(401, description="Invalid token")
        
        if need_enabled and user[0].enabled != 'true':
            abort(401, description="User is not enabled")

        return user

    def authenticate_token(token):
        try:
            username, user_id = Security.decode_jwt(token)
        except Exception as e:
            return False

        user_model = User()
        user = user_model.select(username=username)
        if not user or user[0].id != user_id:
            user = user_model.select(id=user_id)
            if not user:
                return False
        
        return user