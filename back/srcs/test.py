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




def load_key():
    key_file_path = 'secret.key'
    
    # Check if the key file exists
    if not os.path.exists(key_file_path):
        # If it doesn't exist, generate a new key and save it to the file
        with open(key_file_path, 'wb') as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
    
    # Read and return the key from the file
    return open(key_file_path, 'rb').read()


key = load_key()
cipher = Fernet(key)

@bp.route('/api/bye', methods=['GET'])
def bye():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    data = {"bye_world": "Goodbye, Weeeee", 'users': users_list}
    return jsonify(data)

@bp.route('/upload_photo', methods=['POST'])
def upload_photo():
    print("upload_photo------------------------------------------------------------")
    print(request.files)
    user = Auth.authenticate(request)

    # print("user:", user)


    description = request.form.get('text', '')
    if not description or len(description.strip()) == 0 or len(description) > 420:
        abort(400, description="Description is required and must be between 1 and 420 characters.")

    print("description: ", description)
    encrypted_description = cipher.encrypt(description.encode()).decode()
    print("encrypted_description: ", encrypted_description)



    user = user[0]
    user.update({'description': encrypted_description}, {'id': user.id})

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
                    pass  # Just opening to validate
            except Exception as e:
                print("The file is not an image")
                abort(400, description="The file is not an image")
            file.stream.seek(0)  # Reset file pointer to the beginning
            filename = secure_filename(file.filename)
            user_id = user[0].id
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

    return jsonify({"msg": "Files uploaded successfully"})

@bp.route('/delete_photo/<photo_url>', methods=['DELETE'])
def delete_photo(photo_url):
    # Query the database for the photo
    photo = Photo()
    username = 'jareste'
    unique_filename = f"{username}_{photo_url}"
    hashed_filename = hash_to_db(unique_filename) + ".png"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)
    photo_record = photo.select(url=upload_path)
    if not photo_record:
        abort(404, description="Photo not found")

    # Delete the file from the file system
    if os.path.exists(photo_record[0][2]):
        os.remove(photo_record[0][2])
    else:
        print("The file does not exist")

    # Delete the record from the database
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