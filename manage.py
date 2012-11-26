#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import nose
from flask.ext.script import Manager

import settings
from app import app, db
from app.core.models import File
from unistorage import RegularFile as UnistorageRegularFile
from unistorage.client import UnistorageClient, UnistorageError, UnistorageTimeout


manager = Manager(app)


@manager.command
def create_db():
    """Creates all tables."""
    db.create_all()


@manager.command
def update_expiring_files():
    """Updates file entries that will expire in a hour."""
    next_hour = datetime.utcnow() + timedelta(hours=1)

    unistorage = UnistorageClient(settings.UNISTORAGE_URL,
                                  settings.UNISTORAGE_ACCESS_TOKEN)
    for db_file in File.query.filter(File.unistorage_valid_until <= next_hour).all():
        try:
            unistorage_file = unistorage.get_file(db_file.unistorage_resource_uri)
            if not isinstance(unistorage_file, UnistorageRegularFile):
                raise NotRegularFileException()
            
            db_file.unistorage_url = unistorage_file.url
            db_file.unistorage_valid_until = datetime.utcnow() + \
                timedelta(seconds=unistorage_file.ttl) 
            db.session.add(db_file)
            db.session.commit()
        except (UnistorageError, UnistorageTimeout, NotRegularFileException) as e:
            print str(e)


if __name__ == '__main__':
    manager.run()
