from flask import Blueprint, jsonify

bp = Blueprint('test', __name__)

@bp.route('/api/bye', methods=['GET'])
def bye():
    data = {"bye_world": "Goodbye, Weeeee"}
    return jsonify(data)