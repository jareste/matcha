from flask import Blueprint, jsonify, request, abort
from .models import User
from .authenticate import Authenticate as Auth

bp = Blueprint('chat', __name__)

@bp.route('/matches_chat', methods=['GET'])
def get_matches():
    user = Auth.authenticate(request)
    user_id = user[0].id
    user_model = User()
    user = user_model.select(id=user_id)
    user = user[0]

    if not user.matches: # check if friends is empty
        return jsonify({"matches": []})
    matches = user.matches.split(',')
    match_list = []
    for match in matches:
        match_list.append(user_model.select(id=match)[0].username)
    return jsonify({"matches": match_list})

