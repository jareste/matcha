from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from . import routes, test
    app.register_blueprint(routes.bp)
    app.register_blueprint(test.bp)

    return app