from flask import request, abort
from .security import Security
from .models import User

class Authenticate:
    def authenticate(request):
        auth_header = request.headers.get('Authorization')
        print("auth_header: ", auth_header)
        if not auth_header:
            print("No token provided")
            abort(401, description="No token provided")
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

        print(f"token:{token}")
        try:
            username, user_id = Security.decode_jwt(token)
        except Exception as e:
            print("Invalid token1")
            abort(401, description="Invalid token")

        user_model = User()
        user = user_model.select(username=username)
        if not user or user[0][0] != user_id:
            print("Invalid token")
            abort(401, description="Invalid token")
        
        return user