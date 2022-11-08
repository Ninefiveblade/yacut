""" Yacut views module """

from flask import redirect, render_template, flash, url_for

from . import app
from .models import URL_map
from .forms import UrlForm

MESSAGE_FOR_SHORT = "Имя {} уже занято!"
URL_EXISTS = "Такой url уже существует!"


@app.route("/", methods=["GET", "POST"])
def short_url():
    """GET page, POST form, return results in view."""
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    short_link = form.custom_id.data or URL_map.get_unique_short_id()
    original = form.original_link.data
    if URL_map.filter_exists(URL_map.short, short_link):
        flash(MESSAGE_FOR_SHORT.format(short_link))
        return render_template("index.html", form=form)
    if URL_map.filter_exists(URL_map.original, original):
        flash(URL_EXISTS)
        return render_template("index.html", form=form)
    ready_short_link = URL_map.create(original, short_link)
    return render_template("index.html", form=form, link=url_for(
        'short_url_redirect',
        _external=True,
        short_id=ready_short_link.short))


@app.route("/<string:short_id>", methods=["GET"])
def short_url_redirect(short_id):
    """Redirect to original link by short_id"""

    return redirect(URL_map.filter_first_or_404(URL_map.short, short_id).original)
