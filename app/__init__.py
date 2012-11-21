from flask import Flask, session, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy

import settings


app = Flask(__name__)
db = SQLAlchemy(app)

app.config.update(
    DEBUG=settings.DEBUG,
    SECRET_KEY=settings.SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI
)

import users
import core
app.register_blueprint(users.bp)
app.register_blueprint(core.bp)
