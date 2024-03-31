from flask import Blueprint, jsonify, request, abort
from srcs.models import User, Photo, hash_to_db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from PIL import Image
from .security import Security
from .authenticate import Authenticate as Auth

bp = Blueprint('test', __name__)

@bp.route('/api/bye', methods=['GET'])
def bye():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    data = {"bye_world": "Goodbye, Weeeee", 'users': users_list}
    return jsonify(data)

@bp.route('/upload_photo', methods=['POST'])
def upload_photo():
    user = Auth.authenticate(request)

    print("user:", user)
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        print(file.filename)
        try:
            with Image.open(file.stream) as img:
                pass  # Just opening to validate
        except Exception as e:
            print("The file is not an image")
            abort(400, description="The file is not an image")
        file.stream.seek(0)  # Reset file pointer to the beginning
        filename = secure_filename(file.filename)
        username = user[0][0]
        unique_filename = f"{username}_{filename}"
        hashed_filename = hash_to_db(unique_filename) + ".png"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        photo = Photo()
        photo.insert(user_id=username, url=upload_path)
        print("photo saved at: ", upload_path)
        print("username: ", username)
        return jsonify({"msg": "File uploaded successfully", "url": f"/uploads/{hashed_filename}"})
        return 'File uploaded successfully'

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
    if os.path.exists(photo_record[0][1]):
        os.remove(photo_record[0][1])
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
    username = 'jareste'
    unique_filename = f"{username}_{filename}"
    hashed_filename = hash_to_db(unique_filename) + ".png"
    print("showing photo: ", hashed_filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], hashed_filename)