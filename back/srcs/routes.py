from flask import Blueprint, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello World"}
    return jsonify(data)