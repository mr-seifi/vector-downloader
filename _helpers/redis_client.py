from redis import Redis
from .singleton import singleton
from vector_downloader import REDIS_HOST, REDIS_PORT


@singleton
class RedisClient:

    def __init__(self):
        self.redis = Redis(REDIS_HOST, REDIS_PORT)

    def client(self):
        return self.redis


def get_redis_client():
    return RedisClient().client()
