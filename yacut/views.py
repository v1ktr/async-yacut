import asyncio

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.constants import UPLOAD_FAILED_MESSAGE
from yacut.forms import UploadFilesForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import (
    ShortIdError,
    build_short_link,
    choose_short_id,
    get_unique_short_id,
    save_url_map,
)
from yacut.yandex_disk import YandexDiskError, upload_files


def read_files(storages):
    if not isinstance(storages, (list, tuple)):
        storages = [storages] if storages else []
    payloads = []
    for storage in storages:
        filename = getattr(storage, 'filename', None)
        if filename:
            payloads.append((filename, storage.read()))
    return payloads


def save_file_links(stored_files):
    uploaded = []
    for filename, download_url in stored_files:
        short_id = get_unique_short_id()
        db.session.add(URLMap(original=download_url, short=short_id))
        db.session.flush()
        uploaded.append({
            'name': filename,
            'short_link': build_short_link(short_id),
        })
    db.session.commit()
    return uploaded


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_link = None
    if form.validate_on_submit():
        try:
            short_id = choose_short_id(form.custom_id.data)
            save_url_map(form.original_link.data, short_id)
        except ShortIdError as error:
            flash(error.message)
        else:
            short_link = build_short_link(short_id)
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = UploadFilesForm()
    uploaded = []
    if form.validate_on_submit():
        payloads = read_files(form.files.data)
        token = app.config['DISK_TOKEN']
        try:
            stored = asyncio.run(upload_files(payloads, token))
        except YandexDiskError:
            flash(UPLOAD_FAILED_MESSAGE)
        else:
            uploaded = save_file_links(stored)
    return render_template('files.html', form=form, uploaded=uploaded)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
