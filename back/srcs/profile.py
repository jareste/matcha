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
    user_id = user[0].id
    user_model = User()
    user = user_model.select(id=user_id)
    user = user[0]

    photo_model = Photo()
    photo = photo_model.select(user_id=user_id)
    for p in photo:
        print("photo: ", p)

    if photo:
        photoUrl = os.path.basename(photo[0].url) if photo[0].url else 'default.png'
    else:
        photoUrl = 'default.png'

    print("profile_pic: ", photoUrl)
    return jsonify({"username": user.username, "email": user.email, "photoUrl": photoUrl})

@bp.route('/user_photos', methods=['GET'])
def user_photos():
    user = Auth.authenticate(request)
    user_id = user[0].id

    photo_model = Photo()
    photos = photo_model.select(user_id=user_id)

    photo_urls = [os.path.basename(photo.url) for photo in photos if photo.url]
    print('photos:', photo_urls)

    if photos:
        photoUrl = os.path.basename(photos[0].url) if photos[0].url else 'default.png'
    else:
        photoUrl = 'default.png'

    return jsonify({"photos": photo_urls, "username": user[0].username, "photoUrl": photoUrl})
