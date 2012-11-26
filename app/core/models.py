from flask import url_for

from app import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    path = db.Column(db.String(100))
    unistorage_resource_uri = db.Column(db.String(200))
    unistorage_valid_until = db.Column(db.DateTime)
    unistorage_url = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('files', lazy='dynamic'))

    def get_dropbucket_url(self, external=True):
        if self.path:
            return url_for('core.redirect_path', path=self.path, _external=external)
        else:
            return url_for('core.redirect_id', id=self.id, _external=external)
