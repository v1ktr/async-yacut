import random
import re
import string

from flask import url_for
from sqlalchemy.exc import IntegrityError

from yacut import db
from yacut.constants import (
    CUSTOM_ID_PATTERN,
    DUPLICATE_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
    RESERVED_SHORT_IDS,
    SHORT_ID_LENGTH,
)
from yacut.models import URLMap

CUSTOM_ID_RE = re.compile(CUSTOM_ID_PATTERN)
SHORT_ID_ALPHABET = string.ascii_letters + string.digits


class ShortIdError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def random_short_id(length):
    return ''.join(random.choices(SHORT_ID_ALPHABET, k=length))


def get_unique_short_id(length=SHORT_ID_LENGTH):
    short_id = random_short_id(length)
    while URLMap.query.filter_by(short=short_id).first() is not None:
        short_id = random_short_id(length)
    return short_id


def short_id_taken(short_id):
    if short_id in RESERVED_SHORT_IDS:
        return True
    return URLMap.query.filter_by(short=short_id).first() is not None


def validate_custom_id(custom_id):
    if (
        not isinstance(custom_id, str)
        or CUSTOM_ID_RE.fullmatch(custom_id) is None
    ):
        raise ShortIdError(INVALID_SHORT_ID_MESSAGE)
    if short_id_taken(custom_id):
        raise ShortIdError(DUPLICATE_SHORT_ID_MESSAGE)
    return custom_id


def choose_short_id(custom_id):
    if not custom_id:
        return get_unique_short_id()
    return validate_custom_id(custom_id)


def save_url_map(original, short):
    db.session.add(URLMap(original=original, short=short))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ShortIdError(DUPLICATE_SHORT_ID_MESSAGE)
    return short


def build_short_link(short_id):
    return url_for('redirect_view', short_id=short_id, _external=True)
