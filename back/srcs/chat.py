from flask import Blueprint, jsonify, request, abort
from .models import User
from .authenticate import Authenticate as Auth

bp = Blueprint('chat', __name__)

@bp.route('/friends', methods=['GET'])
def get_friends():
    print('get frieeeends')
    user = Auth.authenticate(request)
    user_id = user[0][0]
    user_model = User()
    user = user_model.select(id=user_id)
    user = user[0]

    if not user[6]: # check if friends is empty
        return jsonify({"friends": []})
    friends = user[6].split(',')
    friend_list = []
    for friend in friends:
        friend_list.append(user_model.select(id=friend)[0][1])
    return jsonify({"friends": friend_list})

