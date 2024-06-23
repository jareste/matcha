from flask import Blueprint, jsonify, request, abort
from .models import User
from .authenticate import Authenticate as Auth

bp = Blueprint('match', __name__)

@bp.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    user_id = data.get('user_id')
    liked_user_id = data.get('liked_user_id')
    
    print('like', liked_user_id)    
    user_model = User()
    users = user_model.select(id=user_id)
    if users:
        user = users[0]
        print('liked_user_id', liked_user_id)
        if user.add_like(liked_user_id):
            print('aqui siiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii12312412421')
            return jsonify({"msg": "It's a match!"}), 200
    return jsonify({"msg": "Liked"}), 200

@bp.route('/dislike', methods=['POST'])
def dislike():
    data = request.get_json()
    user_id = data.get('user_id')
    liked_user_id = data.get('liked_user_id')

    print('dislike', liked_user_id)    
    # user_model = User()
    # users = user_model.select(id=user_id)
    # if users:
    #     user = users[0]
    #     if user.like(liked_user_id):
    #         return jsonify({"msg": "It's a match!"}), 200
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
    user = Auth.authenticate(request)
    user_id = user[0].id
    user_model = User()
    user = user_model.select(id=user_id)
    user_random = user[0].select_random()
    print('possible match!!!!!!!!!!!!!!!!!!!')
    #here must come the algorithm to find best match for self user
    print('u32131231323123123eeeeeeeeeeeeeeeeeeeeer')
    counter = 0
    if user_random:
        while user_random.id == user_id:
            if user[0].select_random() == None:
                return jsonify({"user": -1}), 200
            user_random = user[0].select_random()
            counter += 1
            if counter == 10:
                return jsonify({"user": -1}), 200
        print('useeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer',user_random)
        # return jsonify({"user": -1}), 200 #simulates not finding a match for testing purpouses
        return jsonify({"user": user_random.id, "username": user_random.username, "user_photo": 'default.png'}), 200
    return jsonify({"user": -1}), 200
