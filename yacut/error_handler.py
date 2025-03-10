""" Yacut errors_handler module """

from http import HTTPStatus as status

from flask import jsonify, render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), status.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), status.INTERNAL_SERVER_ERROR


class InvalidAPIUsage(Exception):
    """Handle in-exception return jsonable view."""

    status_code = status.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


class UniqueShortIDError(Exception):
    """ Raise error if short_id hash doesn't match """