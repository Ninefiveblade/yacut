""" Yacut forms module """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import InputRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    """ Define a form for prepare and validate users data. """

    original_link = URLField(
        "Добавьте ссылку на обработку",
        validators=[Length(1, 256), InputRequired("Обязательное поле")],
    )
    custom_id = StringField(
        "Ваш вариант ссылки",
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(r"^[A-Za-z0-9]+$", message="string must be alphanumeric"),
        ],
    )
    submit = SubmitField("Создать")
