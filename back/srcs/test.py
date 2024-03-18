from flask import Blueprint, jsonify
from srcs.models import User

bp = Blueprint('test', __name__)

@bp.route('/api/bye', methods=['GET'])
def bye():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    data = {"bye_world": "Goodbye, Weeeee", 'users': users_list}
    return jsonify(data)