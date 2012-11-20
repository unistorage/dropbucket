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

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': settings.FACEBOOK_CONSUMER_KEY,
    'consumer_secret': settings.FACEBOOK_CONSUMER_SECRET
}

app.config['SECURITY_POST_LOGIN'] = '/lala'

from users.models import User, Role, Connection

security = Security(app, SQLAlchemyUserDatastore(db, User, Role))
social = Social(app, SQLAlchemyConnectionDatastore(db, Connection))

import users

app.register_blueprint(users.bp, url_prefix='/users/')

class SocialLoginError(Exception):
    def __init__(self, provider):
        self.provider = provider


@app.before_first_request
def before_first_request():
    try:
        models.db.create_all()
    except Exception, e:
        app.logger.error(str(e))

@login_failed.connect_via(app)
def on_login_failed(sender, provider, oauth_response):
    app.logger.debug('Social Login Failed via %s; '
                     '&oauth_response=%s' % (provider.name, oauth_response))

    # Save the oauth response in the session so we can make the connection
    # later after the user possibly registers
    session['failed_login_connection'] = \
        get_conection_values_from_oauth_response(provider, oauth_response)

    raise SocialLoginError(provider)


@app.errorhandler(SocialLoginError)
def social_login_error(error):
    print 'error', error
    return redirect(
        url_for('register', provider_id=error.provider.id, login_failed=1))
