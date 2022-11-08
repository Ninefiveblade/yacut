""" Yacut api views module """

from http import HTTPStatus
import re

from flask import jsonify, request

from . import app
from .error_handler import InvalidAPIUsage
from .models import URL_map
from .constants import SHORT_CHECK, MAX_LENGHT_SHORT

EMPTY_BODY = "Отсутствует тело запроса"
EMPTY_URL = '"url" является обязательным полем!'
WRONG_CUSTOM_ID = "Указано недопустимое имя для короткой ссылки"
NOT_FOUND_CUSTOM_ID = "Указанный id не найден"
OCCUPIED_CUSTOM_ID = 'Имя "{}" уже занято.'


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_short_url(short_id):
    """Get parent url by short url for redirect."""

    custom_id = URL_map.filter_first(URL_map.short, short_id)
    if custom_id is not None:
        return jsonify(custom_id.get_link_to_dict()), HTTPStatus.OK
    raise InvalidAPIUsage(NOT_FOUND_CUSTOM_ID, HTTPStatus.NOT_FOUND)


@app.route("/api/id/", methods=["POST"])
def add_short_url():
    """Create short url by entered URL."""

    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(EMPTY_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    original = data.get('url')
    custom_id = data.get('custom_id')
    if custom_id is not None:
        if custom_id == "":
            custom_id = URL_map.get_unique_short_id()
        elif not re.fullmatch(SHORT_CHECK, custom_id) or\
                len(custom_id) > MAX_LENGHT_SHORT:
            raise InvalidAPIUsage(WRONG_CUSTOM_ID)
        if URL_map.filter_exists(URL_map.short, custom_id):
            raise InvalidAPIUsage(OCCUPIED_CUSTOM_ID.format(custom_id))
    else:
        custom_id = URL_map.get_unique_short_id()
    url = URL_map.create(original, custom_id)
    return url.create_link_to_dict(), HTTPStatus.CREATED
