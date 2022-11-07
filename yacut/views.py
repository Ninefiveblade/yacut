""" Yacut views module """

from flask import redirect

from . import app
from .models import URL_map


@app.route("/", methods=["GET", "POST"])
def short_url():
    """GET page, POST form, return results in view."""

    return URL_map.create()


@app.route("/<string:short_id>", methods=["GET"])
def short_url_redirect(short_id):
    """Redirect to original link by short_id"""

    link = URL_map.filter_first_or_404(URL_map.short, short_id)
    return redirect(link.original)
