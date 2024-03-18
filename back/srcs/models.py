from . import db
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username

def store_username(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()

with current_app.app_context():
    db.create_all()