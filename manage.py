#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nose
from flask.ext.script import Manager

from app import app, db


manager = Manager(app)

@manager.command
def create_db():
    """Creates all tables."""
    db.create_all()

    
if __name__ == '__main__':
    manager.run()
