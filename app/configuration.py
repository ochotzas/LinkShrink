import logging

EXPIRE_LINKS_CHECK_TIME_SEC = 30  # 30 seconds
EXPIRE_LINKS_TIME_SEC = 60  # 60 seconds
APP_SECRET_KEY = 'your_secret_key'
DB_FILE = 'app/db/urls.json'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)

