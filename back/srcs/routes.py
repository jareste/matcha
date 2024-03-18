from flask import Blueprint, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/api/data', methods=['GET'])
def get_data():
    from srcs.models import store_username
    store_username("tesEEEEEEEEt")
    data = {"message": "Hello Worldssssssssssssss"}
    return jsonify(data)