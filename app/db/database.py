import os
import threading
from contextlib import contextmanager
from typing import Dict, List, Tuple, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.common.enums.url_prop import UrlProperties
from app.configuration import DB_URL, logging
from app.models.url import URLModel, Base

if DB_URL.startswith('sqlite'):
    db_path = DB_URL.replace('sqlite:///', '')
    if db_path:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_engine(DB_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        session.close()

def init_db():
    Base.metadata.create_all(engine)
    logging.info("Database initialized successfully")

def save_url(short_url: str, url_info: Dict):
    with get_db_session() as session:
        url = session.query(URLModel).filter_by(short_url=short_url).first()
        if url:
            url.original_url = url_info.get(UrlProperties.ORIGINAL_URL.value, url.original_url)
            url.expired = url_info.get(UrlProperties.EXPIRED.value, url.expired)
            url.visits = url_info.get(UrlProperties.VISITS.value, url.visits)
            url.creator = url_info.get(UrlProperties.CREATOR.value, url.creator)
            url.expiration_time = url_info.get(UrlProperties.EXPIRATION_TIME.value, url.expiration_time)
        else:
            url = URLModel.from_dict(short_url, url_info)
            session.add(url)
        logging.debug(f"Saved URL: {short_url}")

def get_url(short_url: str) -> Optional[Dict]:
    with get_db_session() as session:
        url = session.query(URLModel).filter_by(short_url=short_url).first()
        if url:
            return url.to_dict()
        return None

def get_all_urls() -> Dict[str, Dict]:
    with get_db_session() as session:
        urls = session.query(URLModel).all()
        return {url.short_url: url.to_dict() for url in urls}

def increment_url_visit(short_url: str) -> bool:
    with get_db_session() as session:
        url = session.query(URLModel).filter_by(short_url=short_url).first()
        if url:
            url.visits += 1
            return True
        return False

def get_expiration_heap() -> List[Tuple[float, str]]:
    with get_db_session() as session:
        urls = session.query(URLModel.expiration_time, URLModel.short_url).filter_by(expired=False).all()
        return [(url.expiration_time, url.short_url) for url in urls]

def expire_url(short_url: str) -> bool:
    with get_db_session() as session:
        url = session.query(URLModel).filter_by(short_url=short_url).first()
        if url:
            url.expired = True
            return True
        return False

def get_user_urls(user_identifier: str) -> List[Dict]:
    with get_db_session() as session:
        urls = session.query(URLModel).filter_by(creator=user_identifier).all()
        return [{'short_url': url.short_url, **url.to_dict()} for url in urls]

def close_connections():
    Session.remove()

def update_url_status(short_url, status):
    try:
        with get_db_session() as session:
            url = session.query(URLModel).filter_by(short_url=short_url).first()
            if not url:
                logging.warning(f"URL not found for status update: {short_url}")
                return False
            if status == "expired":
                url.expired = True
            elif status == "active":
                url.expired = False
            else:
                logging.warning(f"Unsupported URL status: {status}")
                return False
            logging.info(f"Updated status for {short_url} to {status}")
            return True
    except Exception as e:
        logging.error(f"Error updating URL status: {e}")
        return False
