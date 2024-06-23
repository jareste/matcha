from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Photo
from flask import Blueprint, request, jsonify, abort
from flask import app
from .security import Security
import os
import re

bp = Blueprint('login', __name__)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    match = re.match(email_regex, email)
    return bool(match)


@bp.route('/register', methods=['POST'])
def register():
    print("register")
    print(request.json)
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    age = request.json.get('age', None)
    password = request.json.get('password', None)
    password_confirmation = request.json.get('password_confirmation', None)

    if not username or not email or not password or not password_confirmation or not age or int(age) < 18 or int(age) > 120:
        print("Missing required fields")
        abort(400, description="Missing required fields")
        # return jsonify({"msg": "Missing required fields"}), 400

    if password != password_confirmation:
        print("Passwords do not match")
        abort(400, description="Passwords do not match")
        # return jsonify({"msg": "Passwords do not match"}), 400

    if not is_valid_email(email):
        abort(400, description="Email is not valid.")

    user_model = User()
    existing_user = user_model.select(username=username)
    if existing_user:
        print("Username already exists")
        abort(400, description="Username already exists")
        # return jsonify({"msg": "Username already exists"}), 400

    existing_email = user_model.select(email=email)
    if existing_email:
        print("Email already exists")
        abort(400, description="Email already exists")
        # return jsonify({"msg": "Email already exists"}), 400

    secure, msg = Security.check_password(password)
    if secure is False:
        print(msg)
        abort(400, description=msg) 

    print("age,", age)
    try:
        hashed_password = generate_password_hash(password)
        user_model.insert(username=username, email=email, password=hashed_password, age=age)

        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        abort(500, description=str(e))
        # return jsonify({"msg": str(e)}), 500

# @bp.route('/login', methods=['POST'])
# def login():
#     print(type(app))
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#     user_model = User()
#     user = user_model.select(username=username)


#     print("user: ", user.id())
#     if user and check_password_hash(user[0][3], password):  # user[0][2] is the password field
#         access_token = Security.create_jwt(user[0][1], user[0][0])
        
#         user_model.update(updates={'jwt': access_token}, conditions={'username': username})

#         users = user_model.select()
#         for u in users:
#             print(u) 

#         photo_model = Photo()
#         photo = photo_model.select(user_id=user[0][0])
#         for p in photo:
#             print("photo: ", p)
#         photoUrl = os.path.basename(photo[0][2]) if photo and len(photo[0]) > 2 else 'default.png'   


#         # user[0].add_friend("jareste")
#         return jsonify({"msg": "OK", "access_token": access_token, "username": username, "photoUrl": photoUrl}), 200

#     print("Bad username or password")
#     abort(401, description="Bad username or password")
#     # return jsonify({"msg": "Bad username or password"}), 401


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user_model = User()
    users = user_model.select(username=username)
    print('users', users)
    if users:
        user = users[0]  # Assume username is unique and get the first match
        if check_password_hash(user.password, password):
            access_token = Security.create_jwt(user.username, user.id)
            
            user_model.update(updates={'jwt': access_token}, conditions={'username': username})

            all_users = user_model.select()
            for u in all_users:
                print(u) 

            photo_model = Photo()
            photos = photo_model.select(user_id=user.id)
            for p in photos:
                print("photo: ", p)
            photoUrl = os.path.basename(photos[0].url) if photos and len(photos[0].url) > 2 else 'default.png'

            return jsonify({"msg": "OK", "access_token": access_token, "username": username, "photoUrl": photoUrl}), 200

    print("Bad username or password")
    abort(401, description="Bad username or password")

