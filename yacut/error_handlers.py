from http import HTTPStatus

from flask import jsonify, render_template, request

from yacut import app, db
from yacut.constants import ID_NOT_FOUND_MESSAGE


def is_api_request():
    return request.path.startswith('/api/')


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    if is_api_request():
        response = {'message': ID_NOT_FOUND_MESSAGE}
        return jsonify(response), HTTPStatus.NOT_FOUND
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    if is_api_request():
        response = {'message': 'Внутренняя ошибка сервера'}
        return jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
