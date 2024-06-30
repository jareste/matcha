from flask import Blueprint, jsonify, request, abort
from srcs.models import User, Photo, hash_to_db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from PIL import Image
from .security import Security
from .authenticate import Authenticate as Auth
import time
from cryptography.fernet import Fernet

bp = Blueprint('test', __name__)

##
def load_key():
    key_file_path = '.secret.key'
    
    if not os.path.exists(key_file_path):
        with open(key_file_path, 'wb') as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
    
    return open(key_file_path, 'rb').read()

##
key = load_key()
cipher = Fernet(key)

##
@bp.route('/api/bye', methods=['GET'])
def bye():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    data = {"bye_world": "Goodbye, Weeeee", 'users': users_list}
    return jsonify(data)

##
@bp.route('/upload_photo', methods=['POST'])
def upload_photo():
    print("upload_photo------------------------------------------------------------")
    print(request.files)
    user = Auth.authenticate(request)

    description = request.form.get('text', '')
    if not description or len(description.strip()) == 0 or len(description) > 420:
        abort(400, description="Description is required and must be between 1 and 420 characters.")

    print("description: ", description)
    encrypted_description = cipher.encrypt(description.encode()).decode()
    print("encrypted_description: ", encrypted_description)

    user = user[0]
    user.update({'description': encrypted_description}, {'id': user.id})

    tags = request.form.get('tags', '')
    tags_list = tags.split(',')
    if tags_list and tags_list[0] != '':
        try:
            user.add_tags(tags_list)
        except ValueError as e:
            abort(400, description=str(e))
    else:
        user.add_tags([])


    gender = request.form.get('gender', '')
    prefered_gender = request.form.get('preferredGender', '')
    username = request.form.get('username', '')
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    age_min = request.form.get('ageMin', '')
    age_max = request.form.get('ageMax', '')
    enabled = request.form.get('enabled', '')
    if enabled == 'true':
        if user.completed == 'false':
            enabled = 'false' # maybe also some message to the user?

    user.update({'gender': gender, 'preference': prefered_gender, 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'age_max': age_max, 'age_min': age_min, 'enabled': enabled}, {'id': user.id})

    for i in range(5):  # Assuming a maximum of 5 files
        file_key = f'image{i}'
        if file_key not in request.files:
            continue
        file = request.files[file_key]
        if file.filename == '':
            continue
        if file:
            print('uploaded:', file.filename)
            try:
                with Image.open(file.stream) as img:
                    pass
            except Exception as e:
                print("The file is not an image")
                abort(400, description="The file is not an image")
            file.stream.seek(0)
            filename = secure_filename(file.filename)
            user_id = user.id
            unique_filename = f"{user_id}_{filename}_{time.time()}" 
            hashed_filename = hash_to_db(unique_filename) + ".png"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            photo = Photo()
            photos = photo.select(user_id=user_id)
            if i < len(photos):
                os.remove(photos[i].url)
                photo.delete(id=photos[i].id)

            photo.insert(user_id=user_id, url=upload_path)
            photo.connection.commit()
            print("photo saved at: ", upload_path)
            print("username: ", user_id)

    access_token = Security.create_jwt(user.username, user.id)
            
    user.update({'jwt': access_token}, {'id': user.id})
    # user.update(updates={'jwt': access_token}, conditions={'username': username})

    return jsonify({"msg": "Files uploaded successfully", "access_token": access_token})

##
@bp.route('/delete_photo/<photo_url>', methods=['DELETE'])
def delete_photo(photo_url):
    photo = Photo()
    username = 'jareste'
    unique_filename = f"{username}_{photo_url}"
    hashed_filename = hash_to_db(unique_filename) + ".png"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)
    photo_record = photo.select(url=upload_path)
    if not photo_record:
        abort(404, description="Photo not found")

    if os.path.exists(photo_record[0][2]):
        os.remove(photo_record[0][2])
    else:
        print("The file does not exist")

    try:
        photo.delete(url=upload_path)
    except Exception as e:
        abort(500, description="There was an issue deleting the photo")

    return 'Photo deleted successfully'

from flask import send_from_directory

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    # user = Auth.authenticate(request)
    # user_id = user[0][0]
    # unique_filename = f"{user_id}_{filename}"
    # hashed_filename = hash_to_db(unique_filename) + ".png"
    print("showing photo: ", filename)
    print("---------------------------------------------------")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)