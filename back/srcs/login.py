from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Photo
from flask import Blueprint, request, jsonify, abort
from flask import app
import requests
from .security import Security
import os
import re

bp = Blueprint('login', __name__)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    match = re.match(email_regex, email)
    return bool(match)

def is_valid_username(username):
    allowed_characters = re.compile(r'^[a-zA-Z0-9_ \-]+$')
    return bool(allowed_characters.match(username))


@bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    email = request.json.get('email', None)
    age = request.json.get('age', None)
    password = request.json.get('password', None)
    password_confirmation = request.json.get('password_confirmation', None)

    #checks
    if not username or not email or not password or not password_confirmation or not age or int(age) < 18 or int(age) > 120:
        abort(400, description="Missing required fields")

    if not first_name or not last_name:
        abort(400, description="Missing required fields")

    if password != password_confirmation:
        abort(400, description="Passwords do not match")

    if not is_valid_username(username):
        abort(400, description="Username is not valid")

    if not is_valid_username(first_name) or not is_valid_username(last_name):
        abort(400, description="First and last name must be alphanumeric")

    if not is_valid_email(email):
        abort(400, description="Email is not valid.")

    user_model = User()
    existing_user = user_model.select(username=username)
    if existing_user:
        abort(400, description="Username already exists")

    existing_email = user_model.select(email=email)
    if existing_email:
        abort(400, description="Email already exists")

    secure, msg = Security.check_password(password)
    if secure is False:
        abort(400, description=msg) 

    try:
        hashed_password = generate_password_hash(password)
        user_model.insert(username=username, email=email, password=hashed_password, age=age, first_name=first_name, last_name=last_name, fame=1000, enabled='false', completed='false')

        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        abort(500, description=str(e))

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
            # for u in all_users:
            #     print(u) 
            
            ip_address = request.remote_addr
            # ip_address = '95.127.43.66'#get ip so i can get location
            response = requests.get(f'http://ipinfo.io/{ip_address}/json?token=84b405eef28ede')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(response.json())

            photo_model = Photo()
            photos = photo_model.select(user_id=user.id)
            # for p in photos:
            #     print("photo: ", p)
            photoUrl = os.path.basename(photos[0].url) if photos and len(photos[0].url) > 2 else 'default.png'

            return jsonify({"msg": "OK", "access_token": access_token, "username": username, "photoUrl": photoUrl}), 200

    print("Bad username or password")
    abort(401, description="Bad username or password")

