from enum import Enum


class Routes(Enum):
    INDEX = '/'
    REDIRECT = '/<short_id>'
    USER = '/user'
