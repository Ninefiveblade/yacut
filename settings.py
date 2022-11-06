""" Flask settings module """

import os
import uuid


class Config(object):
    """ Define configs for flask app """

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or uuid.uuid4().hex
