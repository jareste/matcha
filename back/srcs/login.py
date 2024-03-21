from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask import Blueprint, request, jsonify
from flask import app

bp = Blueprint('login', __name__)

@bp.route('/register', methods=['POST'])
def register():
    print("register")
    print(request.json)
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    password_confirmation = request.json.get('password_confirmation', None)

    if not username or not email or not password or not password_confirmation:
        return jsonify({"msg": "Missing required fields"}), 400

    if password != password_confirmation:
        return jsonify({"msg": "Passwords do not match"}), 400

    user_model = User()
    existing_user = user_model.select(username=username)
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    existing_email = user_model.select(email=email)
    if existing_email:
        return jsonify({"msg": "Email already exists"}), 400

    try:
        hashed_password = generate_password_hash(password)
        user_model.insert(username=username, email=email, password=hashed_password)

        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user_model = User()
    user = user_model.select(username=username)

    if user and check_password_hash(user[0][2], password):  # user[0][2] is the password field
        access_token = create_access_token(identity=username)
        
        user_model.update(updates={'jwt': access_token}, conditions={'username': username})

        users = user_model.select()
        for user in users:
            print(user) 

        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401