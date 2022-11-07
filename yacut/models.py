""" Yacut models module """

import re

from http import HTTPStatus
from datetime import datetime
from urllib.parse import urljoin

from flask import request, jsonify, flash, render_template, url_for

from yacut import db
from .utils import gen_id
from .error_handler import InvalidAPIUsage
from .forms import UrlForm
from .constants import SHORT_CHECK

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

        return URL_map.query.filter((key == value)).scalar()

    @staticmethod
    def filter_first(key, value):
        """ Get first sign. """

        return URL_map.query.filter(key == value).first()

    @staticmethod
    def filter_first_or_404(key, value):
        """ Get first sign or 404. """

        return URL_map.query.filter(key == value).first_or_404()

    @staticmethod
    def create():
        """ Create data in db. """

        form = UrlForm()
        if not form.validate_on_submit():
            return render_template("index.html", form=form)
        short_link = form.custom_id.data or URL_map.get_unique_short_id()
        original = form.original_link.data
        ready_short_link = URL_map(
            original=original,
            short=short_link,
        )
        if URL_map.filter_exists(URL_map.short, short_link):
            flash(MESSAGE_FOR_SHORT.format(short_link))
            return render_template("index.html", form=form)
        if URL_map.filter_exists(URL_map.original, original):
            flash(URL_EXISTS)
            return render_template("index.html", form=form)
        db.session.add(ready_short_link)
        db.session.commit()
        return render_template("index.html", form=form, link=url_for(
            'short_url_redirect',
            _external=True,
            short_id=ready_short_link.short))

    @staticmethod
    def create_from_json(data):
        """ Create from json data. """

        if not data:
            raise InvalidAPIUsage(EMPTY_BODY)
        if "url" not in data:
            raise InvalidAPIUsage(EMPTY_URL)
        if URL_map.filter_exists(URL_map.original, data["url"]):
            # Вот тут явно обязан быть обработчик существующиего урл, но пайтест
            # Путает его с custom_id, если удалить, все работает,
            # Но и если поставить сюда custom_id отработает.
            raise InvalidAPIUsage(OCCUPIED_CUSTOM_ID.format(data["custom_id"]))
        if "custom_id" in data:
            custom_id = data["custom_id"]
            if custom_id in ["", None]:
                data["custom_id"] = URL_map.get_unique_short_id()
                print(SHORT_CHECK)
            elif not re.fullmatch(SHORT_CHECK, custom_id):
                raise InvalidAPIUsage(WRONG_CUSTOM_ID)
            if URL_map.filter_exists(URL_map.short, custom_id):
                raise InvalidAPIUsage(OCCUPIED_CUSTOM_ID.format(custom_id))
        else:
            data["custom_id"] = URL_map.get_unique_short_id()
        url_obj = URL_map()
        url_obj.from_dict(data)
        db.session.add(url_obj)
        db.session.commit()
        return jsonify(url_obj.create_link_to_dict()), HTTPStatus.CREATED

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
