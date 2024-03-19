from . import db
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Association table
# matches = db.Table('matches',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('match_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
# )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, default='')
    email = db.Column(db.String(120), unique=True, nullable=False, default='')
    password = db.Column(db.String(120), nullable=False, default='')
    online = db.Column(db.Boolean, nullable=False, default=False)
    mmr = db.Column(db.Integer, nullable=False, default=1000)
    jwt = db.Column(db.String(120), nullable=True, default='')
    validated = db.Column(db.Boolean, nullable=False, default=False)

    # # Define the relationship to User itself
    # matches = db.relationship('User',
    #                           secondary=matches,
    #                           primaryjoin=id==matches.c.user_id,
    #                           secondaryjoin=id==matches.c.match_id,
    #                           backref='matched_by')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


def store_username(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()

with current_app.app_context():
    db.create_all()