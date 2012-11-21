from functools import wraps

from flask import redirect, url_for
from flask.ext.login import current_user


def anonymous_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(url_for('core.index'))
        return f(*args, **kwargs)
    return wrapper
