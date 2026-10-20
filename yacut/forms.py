from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Optional,
    Regexp,
    URL,
    ValidationError,
)

from yacut.constants import CUSTOM_ID_PATTERN, INVALID_SHORT_ID_MESSAGE


def at_least_one_file(form, field):
    files = field.data
    if not isinstance(files, (list, tuple)):
        files = [files] if files else []
    for storage in files:
        if getattr(storage, 'filename', None):
            return
    raise ValidationError('Выберите хотя бы один файл')


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Это поле обязательно'),
            URL(message='Укажите корректную ссылку'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(CUSTOM_ID_PATTERN, message=INVALID_SHORT_ID_MESSAGE),
        ],
    )
    submit = SubmitField('Создать')


class UploadFilesForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[at_least_one_file],
    )
    submit = SubmitField('Загрузить')
