from flask import Blueprint, jsonify, request, abort
from .models import User
from .authenticate import Authenticate as Auth
import math

bp = Blueprint('match', __name__)

# Haversine formula to calculate distance between two points
# on the Earth given their latitude and longitude in decimal degrees.
# Returns the distance in kilometers.
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


@bp.route('/like', methods=['POST'])
def like():
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    user = Auth.authenticate(request)
    data = request.get_json()
    liked_user_id = data.get('liked_user_id')
    
    if user:
        user = user[0]
        if user.add_like(liked_user_id):
            return jsonify({"msg": "It's a match!"}), 200
    return jsonify({"msg": "Liked"}), 200

@bp.route('/dislike', methods=['POST'])
def dislike():
    user = Auth.authenticate(request)
    data = request.get_json()
    liked_user_id = data.get('liked_user_id')

    if user:
        user = user[0]
        if user.add_dislike(liked_user_id):
            return jsonify({"msg": "Disliked"}), 200
    return jsonify({"msg": "disliked"}), 200

@bp.route('/matches/<int:user_id>', methods=['GET'])
def get_matches(user_id):
    user = Auth.authenticate(request)
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
    #here must come the algorithm to find best match for self user
    counter = 0

    recommended = user[0].recommend_users()
    print('recommended:', recommended)
    for u in recommended:
        print('user:::::::::::', u.id)
    
    print('userid:', user[0].id)
    print('userLikes:', user[0].likes)

    matches = user[0].matches.split(',') if user[0].matches else []
    likes = user[0].likes.split(',') if user[0].likes else []
    dislikes = user[0].dislikes.split(',') if user[0].dislikes else []

    print('matches:', matches)
    print('likes:', likes)
    print('dislikes:', dislikes)


    if recommended:
        recommended_users = {
            "msg": "OK",
            "users": [
                {
                    "id": u.id,
                    "username": u.username,
                    "photo": 'http://localhost:5000/uploads/default.png'
                } for u in recommended if u.id != user_id
            ]
        }


        return jsonify(recommended_users), 200

    return jsonify({"msg": "KO"}), 200

    # if user_random:
    #     while user_random.id == user_id:
    #         if user[0].select_random() == None:
    #             return jsonify({"user": -1}), 200
    #         user_random = user[0].select_random()
    #         counter += 1
    #         if counter == 10:
    #             return jsonify({"user": -1}), 200
    #     # return jsonify({"user": -1}), 200 #simulates not finding a match for testing purpouses
    #     return jsonify({"user": user_random.id, "username": user_random.username, "user_photo": 'default.png'}), 200
    # return jsonify({"user": -1}), 200
