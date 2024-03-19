from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import routes, test, models, login
        db.create_all()

    app.register_blueprint(routes.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(login.bp)

    return app