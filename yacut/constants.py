DUPLICATE_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
MISSING_REQUEST_BODY_MESSAGE = 'Отсутствует тело запроса'
MISSING_URL_MESSAGE = '"url" является обязательным полем!'
ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'
UPLOAD_FAILED_MESSAGE = 'Не удалось загрузить файлы. Попробуйте ещё раз.'

SHORT_ID_LENGTH = 6
CUSTOM_ID_PATTERN = r'^[A-Za-z0-9]{1,16}$'
RESERVED_SHORT_IDS = frozenset({'files'})

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
