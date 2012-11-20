#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nose
from flask.ext.script import Manager

from app import app


manager = Manager(app)

if __name__ == '__main__':
    manager.run()
