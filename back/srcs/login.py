from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask import Blueprint, request, jsonify
from flask import app
from sqlalchemy.exc import SQLAlchemyError

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

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"msg": "Email already exists"}), 400

    try:
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201
    except SQLAlchemyError as e:
        return jsonify({"msg": str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Create a new token every time a user logs in
        access_token = create_access_token(identity=username)
        
        # Store the token in the user model
        user.jwt = access_token
        db.session.commit()

        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401