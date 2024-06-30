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
        return jsonify({"photos": photo_urls, "username": user[0].username, "photoUrl": photoUrl, "description": "", "tags": user[0].tags, 'gender': user[0].gender, 'prefered': user[0].preference, 'age': user[0].age, 'first_name': user[0].first_name, 'last_name': user[0].last_name, 'email': user[0].email, 'age_min': user[0].age_min, 'age_max': user[0].age_max, 'fame': user[0].fame, 'enabled': True if user[0].enabled=='true' else False})
        
    decrypted_description = cipher.decrypt(encrypted_description.encode()).decode()
    print("decrypted_description: ", decrypted_description)
    print("description: ", decrypted_description)

    print("age", user[0].age)
    return jsonify({"photos": photo_urls, "username": user[0].username, "photoUrl": photoUrl, "description": decrypted_description, "tags": user[0].tags, 'gender': user[0].gender, 'prefered': user[0].preference, 'age': user[0].age, 'first_name': user[0].first_name, 'last_name': user[0].last_name, 'email': user[0].email, 'age_min': user[0].age_min, 'age_max': user[0].age_max, 'fame': user[0].fame, 'enabled': True if user[0].enabled=='true' else False})


# from flask import Flask, jsonify, request
# import os
# from models import Auth, Photo, User  # Adjust import according to your project structure
# from cryptography.fernet import Fernet

# app = Flask(__name__)

# # Define the cipher for decrypting descriptions
# cipher = Fernet(b'your-secret-key-here')  # Replace with your actual secret key

@app.route('/profile/<username>', methods=['GET'])
def user_photos(username):
    Auth.authenticate(request)

    user_model = User()
    user = user_model.select(username=username)
    print("user: ", username)
    # user = User.query.filter_by(username=username).first()  # Adjust query based on your ORM
    if not user:
        abort(401, description="User not found")

    user = user[0]
    user_id = user.id
    photo_model = Photo()
    photos = photo_model.select(user_id=user_id)

    photo_urls = [os.path.basename(photo.url) for photo in photos if photo.url]

    photoUrl = os.path.basename(photos[0].url) if photos and photos[0].url else 'default.png'


    encrypted_description = user.description
    decrypted_description = cipher.decrypt(encrypted_description.encode()).decode() if encrypted_description else ''

    response = {
        "photos": photo_urls,
        "username": user.username,
        "photoUrl": photoUrl,
        "description": decrypted_description,
        "tags": user.tags,
        'gender': user.gender,
        'prefered': user.preference,
        'age': user.age,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'age_min': user.age_min,
        'age_max': user.age_max,
        'fame': user.fame,
        'enabled': True if user.enabled == 'true' else False
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
