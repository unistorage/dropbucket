# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import render_template, request, redirect, flash, url_for, abort
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
from unistorage import (RegularFile as UnistorageRegularFile,
                        PendingFile as UnistoragePendingFile)
from unistorage.client import UnistorageClient, UnistorageError, UnistorageTimeout

import settings
from app import db
from .models import File
from .forms import FileForm
from .utils import UnexpectedFileException
from . import bp


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/', methods=['POST'])
@login_required
def create_file():
    user_file = request.files.get('file')
    if not user_file:
        return redirect(url_for('core.index'))

    unistorage = UnistorageClient(settings.UNISTORAGE_URL,
                                  settings.UNISTORAGE_ACCESS_TOKEN)
    try:
        unistorage_file = unistorage.upload_file(
            user_file.filename, user_file, type_id=current_user.id)

        db_file = File()
        db_file.user = current_user
        db_file.name = unistorage_file.name
        db_file.unistorage_resource_uri = unistorage_file.resource_uri

        if isinstance(unistorage_file, UnistoragePendingFile):
            raise UnexpectedFileException()

        if isinstance(unistorage_file, UnistorageRegularFile):
            db_file.unistorage_valid_until = None
        else:
            db_file.unistorage_valid_until = timedelta(seconds=unistorage_file.ttl)

        db_file.unistorage_url = unistorage_file.url
        db.session.add(db_file)
        db.session.commit()
    except (UnistorageError, UnistorageTimeout, UnexpectedFileException):
        flash(u'Во время загрузки файла произошла ошибка. Попробуйте позже.')

    return redirect(url_for('.index'))


@bp.route('/file/<id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_file(id):
    file = File.query.get(id) or abort(404)
    if file.user != current_user:
        abort(403)
    form = FileForm(obj=file)
    if form.validate_on_submit():
        form.populate_obj(file)
        db.session.add(file)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('edit_file.html', form=form)


@bp.route('/file/<id>/remove/', methods=['GET'])
@login_required
def remove_file(id):
    file = File.query.get(id) or abort(404)
    if file.user != current_user:
        abort(403)
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/id/<int:id>')
def redirect_id(id):
    file = File.query.get(id) or abort(404)
    return redirect(file.unistorage_url)


@bp.route('/<path:path>')
def redirect_path(path):
    file = File.query.filter(File.path == path).first() or abort(404)
    return redirect(file.unistorage_url)
