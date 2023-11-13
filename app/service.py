import heapq
import threading
import time
from threading import Timer

from app.common.enums.url_prop import UrlProperties
from app.configuration import EXPIRE_LINKS_CHECK_TIME_SEC
from app.configuration import logging
from app.utils.shorten import load_urls, save_urls


def expire_links():
    logging.info("Expiration thread started.")
    with urls_lock:
        current_time = time.time()
        logging.debug(f"Current time: {current_time}")

        while expiration_heap and expiration_heap[0][0] <= current_time:
            expiration_time, short_url = heapq.heappop(expiration_heap)
            logging.debug(f"Link to expire: {short_url}, Expiration time: {expiration_time}")

            urls = load_urls()
            if short_url in urls:
                urls[short_url][UrlProperties.EXPIRED.value] = True
                save_urls(urls)
                logging.info(f"Link expired: {short_url}")
            else:
                logging.warning(f"Attempting to expire non-existent link: {short_url}")

        next_expiration_time = current_time + EXPIRE_LINKS_CHECK_TIME_SEC
        logging.debug(f"Scheduling next expiration check at: {next_expiration_time}")
        Timer(EXPIRE_LINKS_CHECK_TIME_SEC, expire_links).start()


def check_missed_expirations():
    logging.info("Missed expirations thread started.")
    with urls_lock:
        current_time = time.time()
        logging.debug(f"Current time: {current_time}")

        urls = load_urls()
        for short_url, properties in urls.items():
            expiration_time = properties.get(UrlProperties.EXPIRATION_TIME.value, 0)

            if expiration_time <= current_time and not properties.get(UrlProperties.EXPIRED.value, False):
                properties[UrlProperties.EXPIRED.value] = True
                save_urls(urls)
                logging.info(f"Missed expiration for link: {short_url}")

        next_expiration_time = current_time + EXPIRE_LINKS_CHECK_TIME_SEC
        logging.debug(f"Scheduling next missed expiration check at: {next_expiration_time}")
        Timer(EXPIRE_LINKS_CHECK_TIME_SEC, check_missed_expirations).start()


urls_lock = threading.Lock()
expiration_heap = []

Timer(EXPIRE_LINKS_CHECK_TIME_SEC, expire_links).start()
Timer(EXPIRE_LINKS_CHECK_TIME_SEC, check_missed_expirations).start()
