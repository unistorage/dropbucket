from flask import render_template
from flask.ext.login import current_user, login_required

from . import bp


@bp.route('/')
def index():
    return render_template('index.html')
