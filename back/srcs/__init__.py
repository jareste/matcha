from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask_socketio import SocketIO, send

jwt = JWTManager()
socketio = SocketIO(Flask(__name__), cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        # pass through HTTP errors
        response = e.get_response()
        print(str(e.description))  # Print the description
        response_data = response.get_json()

        new_response_data = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
            "error": True,
        }

        # If the original response data was not None, include it in the new response data
        if response_data is not None:
            new_response_data['original_response'] = response_data

        new_response = jsonify(new_response_data)
        # new_response.status_code = response.status_code
        return new_response


    CORS(app)


    app.config['SECRET_KEY'] = 'secret!'#os.getenv('SECRET_KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['UPLOAD_FOLDER'] = app.root_path + '/media'

    # @socketio.on('message')
    # def handleMessage(msg):
    #     print('Message: ' + msg)
    #     send(msg, broadcast=True)


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