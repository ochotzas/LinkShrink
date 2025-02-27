import logging
import os
from dotenv import load_dotenv


load_dotenv()

ENV = os.getenv('FLASK_ENV', 'production')
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'default-secret-key')

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///linkshrink.db')

MAX_URL_LENGTH = int(os.getenv('MAX_URL_LENGTH', 2000))
DEFAULT_EXPIRATION_DAYS = int(os.getenv('DEFAULT_EXPIRATION_DAYS', 30))

PROXY_COUNT = int(os.getenv('PROXY_COUNT', 0))
SSL_REDIRECT = os.getenv('SSL_REDIRECT', 'False').lower() == 'true'

EXPIRE_LINKS_CHECK_TIME_SEC = int(os.getenv('EXPIRE_LINKS_CHECK_TIME_SEC', 60))
EXPIRE_LINKS_TIME_SEC = int(os.getenv('EXPIRE_LINKS_TIME_SEC', 60))

DB_DIRECTORY = os.getenv('DB_DIRECTORY', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'data'))
os.makedirs(DB_DIRECTORY, exist_ok=True)
DB_FILE = os.path.join(DB_DIRECTORY, os.getenv('DB_FILENAME', 'urls.sqlite'))
DB_URL = f'sqlite:///{DB_FILE}'

TOKEN_COOKIE_NAME = os.getenv('TOKEN_COOKIE_NAME', 'identifier')

logs_dir = os.getenv('LOGS_DIRECTORY', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs'))
os.makedirs(logs_dir, exist_ok=True)

log_level = os.getenv('LOG_LEVEL', 'DEBUG')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, 'app.log'))
    ]
)

