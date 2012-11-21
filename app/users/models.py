from flask.ext.login import UserMixin

from app import db


class User(db.Model, UserMixin):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    oauth_app = db.Column(db.String(20))
    oauth_user_id = db.Column(db.Integer)
    oauth_token = db.Column(db.String(200))
    oauth_secret = db.Column(db.String(200))

    def __init__(self, name, oauth_app, oauth_user_id):
        self.name = name
        self.oauth_app = oauth_app 
        self.oauth_user_id = oauth_user_id
