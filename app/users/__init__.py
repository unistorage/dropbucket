# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.login import LoginManager

from models import User


bp = Blueprint('users', __name__)

@bp.record
def configure(state):
    app = state.app
    
    login_manager = LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


from .views import *
