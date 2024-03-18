from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    # Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        from . import routes, test, models  # move the import here
        db.create_all()

    app.register_blueprint(routes.bp)
    app.register_blueprint(test.bp)

    return app