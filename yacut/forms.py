""" Yacut forms module """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import InputRequired, Length, Optional, Regexp

from .constants import CUSTOM_ID_FORM_CHECK, MAX_LENGHT

REQUIRED_FIELD = "Обязательное поле!"
WRONG_STRING_FORMAT = (
    "Строка должна включать только английские символы и цифры!"
)


class UrlForm(FlaskForm):
    """ Define a form for prepare and validate users data. """

    original_link = URLField(
        "Добавьте ссылку на обработку",
        validators=[InputRequired(REQUIRED_FIELD)],
    )
    custom_id = StringField(
        "Ваш вариант ссылки",
        validators=[
            Length(max=MAX_LENGHT),
            Optional(),
            Regexp(f'^{CUSTOM_ID_FORM_CHECK}+$', message=WRONG_STRING_FORMAT),
        ],
    )
    submit = SubmitField("Создать")
