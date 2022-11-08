""" Yacut models module """
from datetime import datetime
from urllib.parse import urljoin

from flask import request

from yacut import db
from .utils import gen_id

EMPTY_BODY = "Отсутствует тело запроса"
EMPTY_URL = '"url" является обязательным полем!'
WRONG_CUSTOM_ID = "Указано недопустимое имя для короткой ссылки"
OCCUPIED_CUSTOM_ID = 'Имя "{}" уже занято.'
MESSAGE_FOR_SHORT = "Имя {} уже занято!"
URL_EXISTS = "Такой url уже существует!"


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        """ Get hash unique, check in db. """
        hash = gen_id()
        while URL_map.filter_exists(URL_map.short, hash):
            hash = gen_id()
        return hash

    @staticmethod
    def filter_exists(key, value):
        """ Check sign exists. """

        return URL_map.query.filter(key == value).scalar()

    @staticmethod
    def filter_first(key, value):
        """ Get first sign. """

        return URL_map.query.filter(key == value).first()

    @staticmethod
    def filter_first_or_404(key, value):
        """ Get first sign or 404. """

        return URL_map.query.filter(key == value).first_or_404()

    @staticmethod
    def create(original, short_link):
        """ Create data in db. """

        url = URL_map(
            original=original,
            short=short_link,
        )
        db.session.add(url)
        db.session.commit()
        return url

    def get_link_to_dict(self) -> dict:
        """ Return dictionary for json output get_short_url. """

        return dict(url=self.original)

    def create_link_to_dict(self) -> dict:
        """ Return dicrionary for json output created links. """

        return dict(url=self.original, short_link=urljoin(request.host_url, self.short))

    def from_dict(self, data):
        """ Redefining the dictionary keys at the input
        for model readably fields. """

        self.original = data["url"]
        self.short = data["custom_id"]
