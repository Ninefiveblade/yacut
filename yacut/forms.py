""" Yacut forms module """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import InputRequired, Length, Optional, Regexp

from .constants import (
    PATTERN,
    MAX_LENGHT_SHORT,
    MAX_LENGHT_ORIGINAL
)

REQUIRED_FIELD = "Обязательное поле!"
WRONG_STRING_FORMAT = (
    "Строка должна включать только английские символы и цифры!"
)
CUSTOM_ID_HELP_MSG = "Ваш вариант ссылки"
ORIGINAL_LINK_HELP_MSG = "Добавьте ссылку на обработку"
SUMBIT_HELP_MESSAGE = "Создать"


class UrlForm(FlaskForm):
    """ Define a form for prepare and validate users data. """

    original_link = URLField(
        ORIGINAL_LINK_HELP_MSG,
        validators=[Length(max=MAX_LENGHT_ORIGINAL), InputRequired(REQUIRED_FIELD)],
    )
    custom_id = StringField(
        CUSTOM_ID_HELP_MSG,
        validators=[
            Length(max=MAX_LENGHT_SHORT),
            Optional(),
            Regexp(PATTERN, message=WRONG_STRING_FORMAT),
        ],
    )
    submit = SubmitField(SUMBIT_HELP_MESSAGE)
