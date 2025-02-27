import hashlib
import random
import string
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, List

from flask import request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length

from app.common.enums.url_prop import UrlProperties
from app.configuration import DEFAULT_EXPIRATION_DAYS, MAX_URL_LENGTH, logging
from app.db.database import save_url, get_url, increment_url_visit, get_user_urls as db_get_user_urls


class ShortenForm(FlaskForm):
    url = StringField('URL', validators=[
        DataRequired(),
        URL(message="Invalid URL format"),
        Length(max=MAX_URL_LENGTH, message=f"URL must be less than {MAX_URL_LENGTH} characters")
    ])
    submit = SubmitField('Shorten')


def generate_short_id(url: str) -> str:
    timestamp = str(time.time())
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    hash_input = url + timestamp + random_string
    hash_object = hashlib.md5(hash_input.encode())
    return hash_object.hexdigest()[:6]


def shorten_url(url: str, user_token: str = None) -> Tuple[str, Dict]:
    base_url = request.url_root
    short_id = generate_short_id(url)
    short_url = base_url + short_id
    
    expiration_time = time.time() + (DEFAULT_EXPIRATION_DAYS * 24 * 60 * 60)
    
    url_info = {
        UrlProperties.ORIGINAL_URL.value: url,
        UrlProperties.EXPIRED.value: False,
        UrlProperties.VISITS.value: 0,
        UrlProperties.CREATOR.value: user_token,
        UrlProperties.EXPIRATION_TIME.value: expiration_time
    }
    
    save_url(short_url, url_info)
    logging.info(f"Created shortened URL {short_url} for {url}")
    
    return short_url, url_info


def increment_visit_count(short_url: str) -> None:
    if increment_url_visit(short_url):
        logging.debug(f"Incremented visit count for {short_url}")
    else:
        logging.warning(f"Failed to increment visit count for {short_url}")


def get_user_urls(user_token: str) -> List[Dict]:
    return db_get_user_urls(user_token)


def has_user_urls(user_token: str = None) -> bool:
    if not user_token:
        return False
        
    urls = get_user_urls(user_token)
    return len(urls) > 0
