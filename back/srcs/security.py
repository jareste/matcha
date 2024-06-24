from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

class Security:
    def check_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/~" for char in password):
            return False, "Password must contain at least one special character"
        return True, "Password is secure"
    
    def create_jwt(name, id):
        expires = timedelta(hours=24)
        return create_access_token(identity=name, additional_claims={"user_id": id}, expires_delta=expires)

    def decode_jwt(token):
        decoded_token = decode_token(token)
        print("decoded_token: ", decoded_token)
        name = decoded_token['sub']
        user_id = decoded_token['user_id']
        return name, user_id
