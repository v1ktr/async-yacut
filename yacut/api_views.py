from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (
    ID_NOT_FOUND_MESSAGE,
    MISSING_REQUEST_BODY_MESSAGE,
    MISSING_URL_MESSAGE,
)
from yacut.models import URLMap
from yacut.utils import (
    ShortIdError,
    build_short_link,
    choose_short_id,
    save_url_map,
)


def error_response(message, status=HTTPStatus.BAD_REQUEST):
    return jsonify({'message': message}), status


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response(MISSING_REQUEST_BODY_MESSAGE)
    if 'url' not in data:
        return error_response(MISSING_URL_MESSAGE)
    try:
        short_id = choose_short_id(data.get('custom_id'))
        save_url_map(data['url'], short_id)
    except ShortIdError as error:
        return error_response(error.message)
    payload = {
        'url': data['url'],
        'short_link': build_short_link(short_id),
    }
    return jsonify(payload), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        return error_response(ID_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
