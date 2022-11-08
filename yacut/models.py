""" Yacut models module """
from datetime import datetime
from urllib.parse import urljoin
import random
import re

from flask import request

from yacut import db
from .error_handler import UniqueShortIDError, InvalidAPIUsage
from .constants import (
    MAX_ROWS,
    PATTERN,
    HASH_SIZE,
    MAX_LENGHT_SHORT,
)

EMPTY_BODY = "Отсутствует тело запроса"
EMPTY_URL = '"url" является обязательным полем!'
WRONG_CUSTOM_ID = "Указано недопустимое имя для короткой ссылки"
OCCUPIED_CUSTOM_ID = 'Имя "{}" уже занято.'
MESSAGE_FOR_SHORT = "Имя {} уже занято!"
URL_EXISTS = "Такой url уже существует!"
GET_SHORT_ID_ERROR_MSG = (
    "Невозможно сгенерировать ключ, все последовательности уже заняты."
)


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        """ Get hash unique, check in db. """

        for _ in range(MAX_ROWS):
            hash = ''.join(random.choices(PATTERN, k=HASH_SIZE))
            if not URL_map.filter_exists(URL_map.short, hash):
                return hash
        raise ValueError(GET_SHORT_ID_ERROR_MSG)

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
    def create(original, short_link, flag='http'):
        """ Create data in db. """

        if flag == 'api':
            if short_link is not None and short_link != "":
                if not re.fullmatch(
                    PATTERN, short_link
                ) or len(short_link) > MAX_LENGHT_SHORT:
                    raise InvalidAPIUsage(WRONG_CUSTOM_ID)
                if URL_map.filter_exists(URL_map.short, short_link):
                    raise InvalidAPIUsage(OCCUPIED_CUSTOM_ID.format(short_link))
            else:
                try:
                    short_link = URL_map.get_unique_short_id()
                except ValueError as error:
                    raise UniqueShortIDError(error)
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

        return dict(url=self.original,
                    short_link=urljoin(request.host_url, self.short))

    def from_dict(self, data):
        """ Redefining the dictionary keys at the input
        for model readably fields. """

        self.original = data["url"]
        self.short = data["custom_id"]
