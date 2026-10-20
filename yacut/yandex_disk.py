import asyncio
import urllib.parse

import aiohttp

from yacut.constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL


class YandexDiskError(Exception):
    pass


def extract_disk_path(location):
    decoded = urllib.parse.unquote(location)
    marker = '/disk'
    position = decoded.find(marker)
    if position == -1:
        return decoded
    return decoded[position + len(marker):]


async def request_json(session, method, url, **kwargs):
    async with session.request(method, url, **kwargs) as response:
        if response.status >= 400:
            body = await response.text()
            raise YandexDiskError(body)
        return await response.json()


async def put_file(session, upload_url, content):
    async with session.put(upload_url, data=content) as response:
        if response.status >= 400:
            body = await response.text()
            raise YandexDiskError(body)
        location = response.headers.get('Location')
    if not location:
        raise YandexDiskError('Яндекс Диск не вернул расположение файла')
    return location


async def upload_file(session, filename, content, headers):
    upload_info = await request_json(
        session,
        'GET',
        REQUEST_UPLOAD_URL,
        headers=headers,
        params={'path': 'app:/' + filename, 'overwrite': 'True'},
    )
    location = await put_file(session, upload_info['href'], content)
    download_info = await request_json(
        session,
        'GET',
        DOWNLOAD_LINK_URL,
        headers=headers,
        params={'path': extract_disk_path(location)},
    )
    return filename, download_info['href']


async def upload_files(files, token):
    if not files:
        return []
    headers = {'Authorization': f'OAuth {token}'}
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [
                upload_file(session, name, content, headers)
                for name, content in files
            ]
            return await asyncio.gather(*tasks)
    except aiohttp.ClientError as error:
        raise YandexDiskError(str(error)) from error
