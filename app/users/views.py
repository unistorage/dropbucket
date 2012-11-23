from flask import request, render_template, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from flask_oauth import OAuth
from facebook import GraphAPI

import settings
from app import db
from models import User
from utils import anonymous_user_required
from . import bp


oauth = OAuth()


def get_or_create_and_login_user(data):
    oauth_app = data['app']
    oauth_user_id = data['user_id']
    user = User.query.filter_by(oauth_app=oauth_app,
                                oauth_user_id=oauth_user_id).first()
    if user is None:
        user = User('%s user' % oauth_app, oauth_app, oauth_user_id)

    user.oauth_token = data['token']
    user.oauth_secret = data['secret']
    db.session.add(user)
    db.session.commit()

    login_user(user)


twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=settings.TWITTER_CONSUMER_KEY,
    consumer_secret=settings.TWITTER_CONSUMER_SECRET)
twitter.tokengetter(lambda token=None: None)


@bp.route('/login/twitter_callback')
@twitter.authorized_handler
@anonymous_user_required
def twitter_oauth_authorized(response):
    if response is not None:
        get_or_create_and_login_user({
            'app': 'twitter',
            'user_id': response['user_id'],
            'token': response['oauth_token'],
            'secret': response['oauth_token_secret']
        })
    next_url = url_for('core.index')
    return redirect(next_url)


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=settings.FACEBOOK_CONSUMER_KEY,
    consumer_secret=settings.FACEBOOK_CONSUMER_SECRET,
    request_token_params={'scope': 'email'})
facebook.tokengetter(lambda token=None: None)


@bp.route('/login/facebook_callback')
@facebook.authorized_handler
@anonymous_user_required
def facebook_oauth_authorized(response):
    if response is not None:
        profile = GraphAPI(response['access_token']).get_object('me')
        get_or_create_and_login_user({
            'app': 'facebook',
            'user_id': profile['id'],
            'token': response['access_token'],
            'secret': None
        })
    next_url = url_for('core.index')
    return redirect(next_url)


vk = oauth.remote_app(
    'vk',
    base_url='https://api.vkontakte.ru/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://api.vkontakte.ru/oauth/authorize',
    consumer_key=settings.VK_CONSUMER_KEY,
    consumer_secret=settings.VK_CONSUMER_SECRET)
vk.tokengetter(lambda token=None: None)


@bp.route('/login/vk_callback')
@vk.authorized_handler
@anonymous_user_required
def vk_oauth_authorized(response):
    if response is not None:
        get_or_create_and_login_user({
            'app': 'vk',
            'user_id': response['user_id'],
            'token': response['access_token'],
            'secret': None
        })
    next_url = url_for('core.index')
    return redirect(next_url)


providers = {
    'twitter': twitter,
    'facebook': facebook,
    'vk': vk
}


@bp.route('/login')
@anonymous_user_required
def login():
    provider = request.args.get('provider')

    if provider in providers.keys():
        authorized_handler = 'users.%s_oauth_authorized' % provider
        callback_url = url_for(authorized_handler, _external=True)
        return providers[provider].authorize(callback=callback_url)
    else:
        return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))
