# -*- coding: utf-8 -*-
from flask import Blueprint


bp = Blueprint('core', __name__)
from .views import *
