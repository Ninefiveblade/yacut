""" Yacut api views module """

import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import SHORT_CHECK
from .error_handler import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_short_url(short_id):
    """Get parent url by short url for redirect."""

    short_url = URL_map.query.filter(URL_map.short == short_id).first()
    if short_url is not None:
        return jsonify(short_url.get_link_to_dict()), HTTPStatus.OK
    raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)


@app.route("/api/id/", methods=["POST"])
def add_short_url():
    """Create short url by entered URL."""

    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if "custom_id" in data:
        custom_id = data["custom_id"]
        if custom_id in ["", None]:
            data["custom_id"] = get_unique_short_id()
        elif not re.match(SHORT_CHECK, custom_id):
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")
        if URL_map.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    else:
        data["custom_id"] = get_unique_short_id()
    url_obj = URL_map()
    url_obj.from_dict(data)
    db.session.add(url_obj)
    db.session.commit()
    return jsonify(url_obj.create_link_to_dict()), HTTPStatus.CREATED
