from flask import Blueprint, jsonify, request, abort
from srcs.models import User, Photo, hash_to_db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from PIL import Image

bp = Blueprint('test', __name__)

@bp.route('/api/bye', methods=['GET'])
def bye():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    data = {"bye_world": "Goodbye, Weeeee", 'users': users_list}
    return jsonify(data)

@bp.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            Image.open(file)
        except Exception as e:
            abort(400, description="The file is not an image")
        filename = secure_filename(file.filename)
        hashed_filename = hash_to_db(filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], hashed_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        photo = Photo()
        photo.insert(user_id='jareste', url=upload_path)
        print("photo saved")
        return 'File uploaded successfully'

@bp.route('/delete_photo/<photo_url>', methods=['DELETE'])
def delete_photo(photo_url):
    # Query the database for the photo
    photo = Photo()
    hashed_filename = hash_to_db(photo_url)
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
    hashed_filename = hash_to_db(filename)
    print("showing photo: ", hashed_filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], hashed_filename)