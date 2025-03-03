import heapq
import secrets

from flask import render_template, request, abort, make_response, jsonify

from app import app
from app.common.enums.routes import Routes
from app.common.enums.url_prop import UrlProperties
from app.configuration import logging, TOKEN_COOKIE_NAME
from app.db.database import get_url, save_url
from app.service import urls_lock, expiration_heap
from app.utils.shorten import ShortenForm, shorten_url, increment_visit_count, get_user_urls, has_user_urls
from app.utils.token_manager import get_or_create_user_token, with_user_token


@app.route(Routes.INDEX.value, methods=['GET', 'POST'])
@with_user_token
def index():
    form = ShortenForm()

    if form.validate_on_submit():
        url = form.url.data
        user_token = get_or_create_user_token()
        short_url, url_info = shorten_url(url, user_token)
        
        with urls_lock:
            heapq.heappush(expiration_heap, (url_info[UrlProperties.EXPIRATION_TIME.value], short_url))
        logging.info(f"URL {url} shortened to {short_url}")
        return render_template('index.html', form=form, short_url=short_url, visit_count=0, is_creator=True,
                               has_user_urls=has_user_urls(user_token))

    user_token = get_or_create_user_token()
    return render_template('index.html', form=form, has_user_urls=has_user_urls(user_token))


@app.route(Routes.REDIRECT.value, methods=['GET'])
def redirect_to_original(short_id):
    short_url = request.url_root + short_id
    url_info = get_url(short_url)

    if not url_info:
        logging.info(f"Non-existent short URL requested: {short_url}")
        abort(404)

    original_url = url_info.get(UrlProperties.ORIGINAL_URL.value)
    visit_count = url_info.get(UrlProperties.VISITS.value, 0)

    creator_token = url_info.get(UrlProperties.CREATOR.value)
    current_user_token = request.cookies.get(TOKEN_COOKIE_NAME, '')
    is_creator = (creator_token == current_user_token)

    if url_info and not url_info.get(UrlProperties.EXPIRED.value, False):
        increment_visit_count(short_url)
        logging.info(f"Redirecting to original URL: {original_url}")
        return render_template('redirect.html', original_url=original_url, visit_count=visit_count + 1,
                               is_creator=is_creator)

    if url_info and url_info.get(UrlProperties.EXPIRED.value, False):
        logging.info(f"URL {short_url} has expired")
        return render_template('expired.html', short_url=short_url, visit_count=visit_count, is_creator=is_creator)


@app.route(Routes.USER.value, methods=['GET'])
@with_user_token
def user():
    user_token = get_or_create_user_token()
    user_urls = get_user_urls(user_token)
    logging.info(f"User accessed the user page with token: {user_token}")
    return render_template('user.html', urls=user_urls, UrlProperties=UrlProperties)


@app.route('/api/url-count')
def get_url_count():
    user_token = request.cookies.get(TOKEN_COOKIE_NAME)
    
    if not user_token:
        return jsonify({'count': 0})
    
    user_urls = get_user_urls(user_token)
    url_count = len(user_urls) if user_urls else 0
    
    return jsonify({'count': url_count})


@app.route('/api/reset-identifier', methods=['POST'])
def reset_identifier():
    new_token = secrets.token_hex(16)
    
    response = make_response(jsonify({'success': True, 'message': 'Identifier reset successfully'}))
    response.set_cookie(TOKEN_COOKIE_NAME, new_token, max_age=31536000)
    
    return response


@app.errorhandler(404)
def page_not_found(e):
    logging.info(f"404 error: Page not found")
    return render_template('404.html'), 404
