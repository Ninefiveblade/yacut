""" Yacut api views module """

from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handler import InvalidAPIUsage
from .models import URL_map

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

    data = request.get_json()
    return URL_map.create_from_json(data)
