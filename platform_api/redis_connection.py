import os

import redis


class RedisConnection:
    def __init__(self):
        host = os.getenv('REDIS_HOST', default='localhost')
        port = os.getenv('REDIS_PORT', default=6379)
        self._redis = redis.Redis(host, port, db=0)

    def get_client(self):
        return self._redis
