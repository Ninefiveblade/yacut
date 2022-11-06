""" Yacut views module """

from flask import flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def short_url():
    """GET page, POST form, return results in view."""

    form = UrlForm()
    if form.validate_on_submit():
        short_link = form.custom_id.data or get_unique_short_id()
        original = form.original_link.data
        ready_short_link = URL_map(
            original=original,
            short=short_link,
        )
        if URL_map.query.filter(URL_map.short == short_link).first():
            flash(f"Имя {short_link} уже занято!")
            return render_template("index.html", form=form)
        if URL_map.query.filter(URL_map.original == original).first():
            flash("Такой url уже существует!")
            return render_template("index.html", form=form)
        db.session.add(ready_short_link)
        db.session.commit()
        return render_template("index.html", form=form, link=ready_short_link.short)
    return render_template("index.html", form=form)


@app.route("/<string:short_id>", methods=["GET"])
def short_url_redirect(short_id):
    """Redirect to original link by short_id"""

    link = URL_map.query.filter(URL_map.short == short_id).first_or_404()
    return redirect(link.original)
