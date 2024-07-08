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
    if user:
        user = user[0]
        matched_users = []
        liked_users = []
        disliked_users = []
        if user.matches:
            matches = [int(match_id) for match_id in user.matches.split(',') if match_id]
            matched_users = []
            seen_user_ids = set()
            user_model = User()
            for match_id in matches:
                if match_id == user_id:
                    continue
                if match_id in seen_user_ids:
                    continue
                matched_user = user_model.select(id=match_id)[0]
                seen_user_ids.add(match_id)
                photo = matched_user.photo if matched_user.photo else 'default.png'
                matched_users.append({
                    'id': matched_user.id,
                    'username': matched_user.username,
                    'photo': 'http://localhost:5000/uploads/' + photo,
                })
        if user.likes:
            likes = [int(like_id) for like_id in user.likes.split(',') if like_id]
            liked_users = []
            seen_user_ids = set()
            user_model = User()
            for like_id in likes:
                if like_id == user_id:
                    continue
                if like_id in seen_user_ids:
                    continue
                liked_user = user_model.select(id=like_id)[0]
                seen_user_ids.add(like_id)
                photo = liked_user.photo if liked_user.photo else 'default.png'
                liked_users.append({
                    'id': liked_user.id,
                    'username': liked_user.username,
                    'photo': 'http://localhost:5000/uploads/' + photo,
                })
        if user.dislikes:
            dislikes = [int(dislike_id) for dislike_id in user.dislikes.split(',') if dislike_id]
            disliked_users = []
            seen_user_ids = set()
            user_model = User()
            for dislike_id in dislikes:
                if dislike_id == user_id:
                    continue
                if dislike_id in seen_user_ids:
                    continue
                disliked_user = user_model.select(id=dislike_id)[0]
                seen_user_ids.add(dislike_id)
                photo = disliked_user.photo if disliked_user.photo else 'default.png'
                disliked_users.append({
                    'id': disliked_user.id,
                    'username': disliked_user.username,
                    'photo': 'http://localhost:5000/uploads/' + photo,
                })
        print('matches____:', user.matches)
        print('likes____:', user.likes)
        print('dislikes____:', user.dislikes)
        return jsonify({
            'matches': matched_users,
            'likes': liked_users,
            'dislikes': disliked_users,
        }), 200
    return jsonify({"matches": [], "likes": [], "dislikes": []}), 200


@bp.route('/possible_match', methods=['GET'])
def get_possible_match():
    user = Auth.authenticate(request)

    recommended = user[0].recommend_users()

    
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
                    "photo": 'http://localhost:5000/uploads/' + u.photo if u.photo else 'http://localhost:5000/uploads/default.png',
                } for u in recommended if u.id != user[0].id and str(u.id) not in matches and str(u.id) not in likes and str(u.id) not in dislikes
            ]
        }


        return jsonify(recommended_users), 200

    return jsonify({"msg": "KO"}), 200

