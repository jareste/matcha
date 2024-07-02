from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask_socketio import SocketIO, send

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response_data = response.get_json()

        new_response_data = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
            "error": True,
        }

        if response_data is not None:
            new_response_data['original_response'] = response_data

        new_response = jsonify(new_response_data)
        # new_response.status_code = response.status_code
        return new_response


    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message')
    def handle_message(data):
        print(f"Message from {data['sender_id']} to {data['receiver_id']}: {data['message']}")
        socketio.emit('message', {'message': data['message']}, room=data['receiver_id'])


    CORS(app)


    app.config['SECRET_KEY'] = 'secret!'#os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['UPLOAD_FOLDER'] = app.root_path + '/media'



    jwt.init_app(app)

    with app.app_context():
        from . import routes, test, models, login, profile, chat, match

    app.register_blueprint(routes.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(match.bp)

    return app