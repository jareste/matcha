from flask import Blueprint, jsonify, request
from srcs.models import User, Photo
import os
from werkzeug.utils import secure_filename
from flask import current_app as app

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
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        # Save the file path to the database
        photo = Photo()
        photo.insert(user_id='jareste', url=upload_path)
        return 'File uploaded successfully'


from flask import send_from_directory

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)