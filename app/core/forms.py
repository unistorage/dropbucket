# -*- coding: utf-8 -*-
from flask import current_app
from flask.ext.wtf import Form, TextField, Length, ValidationError

from app import db
from models import File


def validate_path_uniqueness(form, field):
    field.data = field.data.strip('/')
    path = field.data
    if path and File.query.filter(
            db.not_(File.id == form.file_id), File.path == path).count() > 0:
        raise ValidationError(u'Такой путь уже занят.')


def validate_path_availability(form, field):
    path = field.data
    if not path:
        return

    endpoint = None
    try:
        endpoint, endpoint_args = current_app.url_map.bind('/').match(path)
    except:
        pass

    if endpoint and endpoint != 'core.redirect_path':
        raise ValidationError(u'Такой путь уже занят.')


class FileForm(Form):
    path = TextField('URL', validators=[
        Length(max=100), validate_path_uniqueness, validate_path_availability])
    
    def __init__(self, *args, **kwargs):
        file = kwargs.get('obj')
        self.file_id = file and file.id
        super(FileForm, self).__init__(*args, **kwargs)

    def populate_obj(self, obj):
        super(FileForm, self).populate_obj(obj)
