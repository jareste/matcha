from flask import Blueprint, jsonify, request, abort
from srcs.models import User, Photo, hash_to_db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from PIL import Image
from .security import Security
from .authenticate import Authenticate as Auth
from cryptography.fernet import Fernet

bp = Blueprint('profile', __name__)

def load_key():
    key_file_path = '.secret.key'
    
    if not os.path.exists(key_file_path):
        with open(key_file_path, 'wb') as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
    
    return open(key_file_path, 'rb').read()


key = load_key()
cipher = Fernet(key)

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
    return jsonify({"username": user.username, "email": user.email, "photoUrl": photoUrl, "description": user.description})

#Actual getter of profile page hehe
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

    encrypted_description = user[0].description
    if not encrypted_description:
        return jsonify({"photos": photo_urls, "username": user[0].username, "photoUrl": photoUrl, "description": "", "tags": user[0].tags, 'gender': user[0].gender, 'prefered': user[0].preference, 'age': user[0].age})
        
    decrypted_description = cipher.decrypt(encrypted_description.encode()).decode()
    print("decrypted_description: ", decrypted_description)
    print("description: ", decrypted_description)

    print("age", user[0].age)
    return jsonify({"photos": photo_urls, "username": user[0].username, "photoUrl": photoUrl, "description": decrypted_description, "tags": user[0].tags, 'gender': user[0].gender, 'prefered': user[0].preference, 'age': user[0].age})
