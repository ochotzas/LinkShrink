from sqlalchemy import Column, String, Boolean, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

from app.common.enums.url_prop import UrlProperties

Base = declarative_base()

class URLModel(Base):
    __tablename__ = 'urls'

    short_url = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    expired = Column(Boolean, default=False)
    visits = Column(Integer, default=0)
    creator = Column(String)
    expiration_time = Column(Float, nullable=False)

    def to_dict(self):
        return {
            UrlProperties.ORIGINAL_URL.value: self.original_url,
            UrlProperties.EXPIRED.value: self.expired,
            UrlProperties.VISITS.value: self.visits,
            UrlProperties.CREATOR.value: self.creator,
            UrlProperties.EXPIRATION_TIME.value: self.expiration_time
        }

    @classmethod
    def from_dict(cls, short_url, url_info):
        return cls(
            short_url=short_url,
            original_url=url_info.get(UrlProperties.ORIGINAL_URL.value),
            expired=url_info.get(UrlProperties.EXPIRED.value, False),
            visits=url_info.get(UrlProperties.VISITS.value, 0),
            creator=url_info.get(UrlProperties.CREATOR.value),
            expiration_time=url_info.get(UrlProperties.EXPIRATION_TIME.value)
        )
