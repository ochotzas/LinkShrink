from ModelSerializer import ModelSerializer

from app.common.enums.url_prop import UrlProperties


class URLModel:
    def __init__(self, expired: bool, visits: int, original_url: str, creator: str, expiration_time: float):
        self.expired = expired
        self.visits = visits
        self.original_url = original_url
        self.creator = creator
        self.expiration_time = expiration_time

    def __dict__(self):
        return {
            UrlProperties.EXPIRED.value: self.expired,
            UrlProperties.VISITS.value: self.visits,
            UrlProperties.ORIGINAL_URL.value: self.original_url,
            UrlProperties.CREATOR.value: self.creator,
            UrlProperties.EXPIRATION_TIME.value: self.expiration_time
        }

    def to_json(self):
        return ModelSerializer(self).to_json()
