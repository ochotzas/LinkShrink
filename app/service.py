import heapq
import threading
import time
import logging

from app.common.enums.url_prop import UrlProperties
from app.configuration import EXPIRE_LINKS_CHECK_TIME_SEC
from app.db.database import get_expiration_heap, expire_url, update_url_status

urls_lock = threading.Lock()
expiration_heap = []

def init_expiration_heap():
    global expiration_heap
    with urls_lock:
        raw_heap = get_expiration_heap()
        expiration_heap = raw_heap.copy() if raw_heap else []
        heapq.heapify(expiration_heap)
    logging.info(f"Initialized expiration heap with {len(expiration_heap)} URLs")

def process_expirations():
    current_time = time.time()
    expired_count = 0

    with urls_lock:
        while expiration_heap and expiration_heap[0][0] <= current_time:
            expiration_time, short_url = heapq.heappop(expiration_heap)
            if expire_url(short_url):
                update_url_status(short_url, "expired")
                logging.info(f"Expired URL: {short_url}")
                expired_count += 1

    if expired_count:
        logging.info(f"Total expired URLs in this check: {expired_count}")

def expiration_worker():
    while True:
        process_expirations()
        time.sleep(EXPIRE_LINKS_CHECK_TIME_SEC)

def missed_expiration_worker():
    MISS_CHECK_INTERVAL = EXPIRE_LINKS_CHECK_TIME_SEC * 10
    while True:
        current_time = time.time()
        expired_count = 0
        with urls_lock:
            new_heap = []
            while expiration_heap:
                expiration_time, short_url = heapq.heappop(expiration_heap)
                if expiration_time <= current_time:
                    if expire_url(short_url):
                        update_url_status(short_url, "expired")
                        logging.info(f"Found and expired missed URL: {short_url}")
                        expired_count += 1
                else:
                    new_heap.append((expiration_time, short_url))
            expiration_heap.extend(new_heap)
            heapq.heapify(expiration_heap)
        if expired_count:
            logging.info(f"Total missed expirations handled: {expired_count}")
        time.sleep(MISS_CHECK_INTERVAL)

def start_expiration_services():
    init_expiration_heap()

    expiration_thread = threading.Thread(target=expiration_worker, daemon=True)
    expiration_thread.start()

    missed_thread = threading.Thread(target=missed_expiration_worker, daemon=True)
    missed_thread.start()

    logging.info("URL expiration services started")
