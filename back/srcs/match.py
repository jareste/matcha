from flask import Blueprint, jsonify, request, abort
from .models import User
from .authenticate import Authenticate as Auth

bp = Blueprint('match', __name__)

@bp.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    user_id = data.get('user_id')
    liked_user_id = data.get('liked_user_id')
    
    user_model = User()
    users = user_model.select(id=user_id)
    if users:
        user = users[0]
        if user.like(liked_user_id):
            return jsonify({"msg": "It's a match!"}), 200
    return jsonify({"msg": "Liked"}), 200

@bp.route('/matches/<int:user_id>', methods=['GET'])
def get_matches(user_id):
    print('get matcheeeeeeeeeeeeeeeeeeeeeeeeeeeeees')
    user_model = User()
    users = user_model.select(id=user_id)
    if users:
        user = users[0]
        if user.matches:
            matches = [int(match_id) for match_id in user.matches.split(',') if match_id]
            matched_users = [user_model.select(id=match_id)[0].__dict__ for match_id in matches]
            return jsonify({"matches": matched_users}), 200
    return jsonify({"matches": []}), 200


@bp.route('/possible_match', methods=['GET'])
def get_possible_match():
    print('possible match!!!!!!!!!!!!!!!!!!!')
    user_model = User()
    #here must come the algorithm to find best match for self user
    users = user_model.select(id='0')
    if users:
        user = users[0]
        return jsonify({"user": user.id}), 200
    return jsonify({"user": []}), 200
