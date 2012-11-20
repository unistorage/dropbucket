from flask import Flask, session, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore, login_failed
from flask.ext.social.utils import get_conection_values_from_oauth_response
import settings


#def configure_blueprints(app):
app = Flask(__name__)
db = SQLAlchemy(app)


app.config.update(
    DEBUG=True,
    SECRET_KEY='123',
    SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI
)

import users
from users.models import User, Role, Connection

security = Security(app, SQLAlchemyUserDatastore(db, User, Role))
app.register_blueprint(users.bp, url_prefix='/users/')
