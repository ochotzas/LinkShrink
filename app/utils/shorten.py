import json
import os
import time

import shortuuid
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL

from app.common.enums.url_prop import UrlProperties
from app.configuration import DB_FILE, EXPIRE_LINKS_TIME_SEC
from app.models.url import URLModel


class ShortenForm(FlaskForm):
    url = StringField('URL', render_kw={"placeholder": "Enter your URL"}, validators=[URL()])
    submit = SubmitField('Shorten')


def load_urls():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}


def save_urls(urls):
    with open(DB_FILE, 'w') as file:
        json.dump(urls, file, indent=2)


def shorten_url(url):
    short_id = shortuuid.uuid()[:8]
    short_url = request.url_root + short_id

    creator_identifier = request.remote_addr
    return short_url, URLModel(False, 0, url, creator_identifier, time.time() + EXPIRE_LINKS_TIME_SEC).__dict__()


def increment_visit_count(short_url, urls):
    if short_url in urls:
        urls[short_url][UrlProperties.VISITS.value] = urls[short_url].get(UrlProperties.VISITS.value, 0) + 1
        save_urls(urls)


def get_user_urls(urls):
    creator_identifier = request.remote_addr
    user_urls = {}
    for url in urls:
        if urls[url][UrlProperties.CREATOR.value] == creator_identifier:
            expiration_time_value = urls[url][UrlProperties.EXPIRATION_TIME.value]
            local_expiration_time = time.localtime(expiration_time_value)
            formatted_expiration_time = time.strftime('%d/%m/%Y at %H:%M:%S', local_expiration_time)
            urls[url][UrlProperties.EXPIRATION_TIME.value] = formatted_expiration_time
            user_urls[url] = urls[url]
    return dict(reversed(list(user_urls.items())))


def has_user_urls(urls):
    return len(get_user_urls(urls)) > 0
