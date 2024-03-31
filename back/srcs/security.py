from flask_jwt_extended import create_access_token, decode_token

class Security:
    def check_password(password):
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True

    def create_jwt(name, id):
        return create_access_token(identity=name, additional_claims={"user_id": id})

    def decode_jwt(token):
        decoded_token = decode_token(token)
        print("decoded_token: ", decoded_token)
        name = decoded_token['sub']
        user_id = decoded_token['user_id']
        return name, user_id
