from flask import Blueprint, jsonify, request, abort
from srcs.models import User, Photo, hash_to_db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from PIL import Image
from .security import Security
from .authenticate import Authenticate as Auth

bp = Blueprint('profile', __name__)

@bp.route('/getProfile', methods=['GET'])
def getProfile():
    user = Auth.authenticate(request)
    user_id = user[0][0]
    user_model = User()
    user = user_model.select(id=user_id)
    user = user[0]

    photo_model = Photo()
    photo = photo_model.select(user_id=user_id)
    for p in photo:
        print("photo: ", p)
    photoUrl = os.path.basename(photo[0][2]) if photo and len(photo[0]) > 2 else 'default.png'
    print("profile_pic: ", photoUrl)
    return jsonify({"username": user[1], "email": user[2], "photoUrl": photoUrl})

@bp.route('/user_photos', methods=['GET'])
def user_photos():
    user = Auth.authenticate(request)
    user_id = user[0][0]

    photo_model = Photo()
    photos = photo_model.select(user_id=user_id)

    photo_urls = [os.path.basename(photo[2]) for photo in photos if len(photo) > 2]
    print('photos:', photo_urls)
    photoUrl = os.path.basename(photos[0][2]) if photos and len(photos[0]) > 2 else 'default.png'

    return jsonify({"photos": photo_urls, "username": user[0][1], "photoUrl": photoUrl})