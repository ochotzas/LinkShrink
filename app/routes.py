import heapq

from flask import render_template, request

from app import app
from app.common.enums.routes import Routes
from app.common.enums.url_prop import UrlProperties
from app.configuration import logging
from app.service import urls_lock, expiration_heap
from app.utils.shorten import ShortenForm, load_urls, shorten_url, save_urls, increment_visit_count, get_user_urls, \
    has_user_urls


@app.route(Routes.INDEX.value, methods=['GET', 'POST'])
def index():
    form = ShortenForm()
    urls = load_urls()

    if form.validate_on_submit():
        url = form.url.data
        short_url, url_info = shorten_url(url)
        with urls_lock:
            urls[short_url] = url_info
            heapq.heappush(expiration_heap, (url_info[UrlProperties.EXPIRATION_TIME.value], short_url))
            save_urls(urls)
        logging.info(f"URL {url} shortened to {short_url}")
        return render_template('index.html', form=form, short_url=short_url, visit_count=0, is_creator=True,
                               has_user_urls=has_user_urls(urls))

    return render_template('index.html', form=form, has_user_urls=has_user_urls(urls))


@app.route(Routes.REDIRECT.value, methods=['GET'])
def redirect_to_original(short_id):
    urls = load_urls()
    short_url = request.url_root + short_id
    url_info = urls.get(short_url, {})

    original_url = url_info.get(UrlProperties.ORIGINAL_URL.value)
    visit_count = url_info.get(UrlProperties.VISITS.value, 0)

    creator_identifier = url_info.get(UrlProperties.CREATOR.value)

    current_user_identifier = request.remote_addr
    is_creator = (creator_identifier == current_user_identifier)

    if url_info and not url_info.get(UrlProperties.EXPIRED.value, False):
        increment_visit_count(short_url, urls)
        logging.info(f"Redirecting to original URL: {original_url}")
        return render_template('redirect.html', original_url=original_url, visit_count=visit_count + 1,
                               is_creator=is_creator)

    if url_info and url_info.get(UrlProperties.EXPIRED.value, False):
        logging.info(f"URL {short_url} has expired")
        return render_template('expired.html', short_url=short_url, visit_count=visit_count, is_creator=is_creator)


@app.route(Routes.USER.value, methods=['GET'])
def user():
    urls = load_urls()
    user_urls = get_user_urls(urls)
    logging.info(f"User accessed the user page")
    return render_template('user.html', urls=user_urls, UrlProperties=UrlProperties)
